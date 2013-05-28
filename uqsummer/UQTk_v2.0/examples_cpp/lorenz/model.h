#include "PCSet.h"

struct dumpInfo {
	int dumpInt;
	int fdumpInt;
	string dumpfile;
};

// Function declarations

/// \brief Compute RHS of Lorenz model, given the parameters a through c, and
/// the current state u, v, w. Return result in dudt, dvdt, dwdt
void GetRHS(const double& a, const double& b, const double & c, const double& u,
		const double& v, const double& w, double& dudt, double& dvdt,
		double& dwdt);

/// \brief Compute RHS of Lorenz model, given the parameters a through c, and
/// the current state u, v, w. Return result in dudt, dvdt, dwdt
/// The parameter b is considered to be uncertain and is represented with a PC expansion. As a result
/// u, v, w, z, dudt, dvdt, and dwdt are also PCEs.
/// aPCSet contains all parameters of the PC type used
void GetRHS(const PCSet &aPCSet, const double* a, const double* b,
		const double* c, const double* u, const double* v, const double* w,
		double* dudt, double* dvdt, double* dwdt);

/// \brief Move the outputs forward in time with time step dTym, given input parameter vector
void forwardFunctionDt(double* inpParams, double dTym, double* outValues);

/// \brief Forward function from t0 to tf, with time step dTym, given input parameter vector
void forwardFunction(double* inpParams, double t0, double tf, double dTym,
		double* outValues, dumpInfo* outPrint);

void forwardFunction(double* inpParams, double t0, double tf, double dTym,
		double* outValues, dumpInfo* outPrint) {
	bool silent = false;
	if (!outPrint)
		silent = true;

	// Current time
	double tym = t0;
	int step = 0;
	double u = outValues[0];
	double v = outValues[1];
	double w = outValues[2];

	FILE* f_dump;

	if (!silent) {

		// Separator in output
		cout << endl << string(70, '=') << endl;
		cout << "Integration" << endl;
		cout << string(70, '=') << endl << endl;
		// write time, u, v, w to file
		if (!(f_dump = fopen(outPrint->dumpfile.c_str(), "w"))) {
			printf("Could not open file '%s'\n", outPrint->dumpfile.c_str());
			exit(1);
		}
		fprintf(f_dump, "%lg %lg %lg %lg\n", tym, u, v, w);

		// write u, v, w to screen
		cout << "Time Step: " << step << ", time: " << tym;
		cout << ", u: " << u;
		cout << ", v: " << v;
		cout << ", w: " << w;
		cout << endl;
	}

	// Forward run
	while (tym < tf) {
		forwardFunctionDt(inpParams, dTym, outValues);
		tym += dTym;
		step += 1;

		if (!silent) {
			u = outValues[0];
			v = outValues[1];
			w = outValues[2];

			// write time, u, v, w to file
			if (step % outPrint->fdumpInt == 0) {
				fprintf(f_dump, "%lg %lg %lg %lg\n", tym, u, v, w);
			}

			// write u, v, w to screen
			if (step % outPrint->dumpInt == 0) {
				cout << "Time Step: " << step << ", time: " << tym;
				cout << ", u: " << u;
				cout << ", v: " << v;
				cout << ", w: " << w;
				cout << endl;
			}
		}

	}

	if (!silent) {
		// write time, u, v, w to file if not already done so
		if (step % outPrint->fdumpInt != 0) {
			fprintf(f_dump, "%lg %lg %lg %lg\n", tym, u, v, w);
		}

		// write u, v, w to screen if not already done so
		if (step % outPrint->dumpInt != 0) {
			cout << "Time Step: " << step << ", time: " << tym;
			cout << ", u: " << u;
			cout << ", v: " << v;
			cout << ", w: " << w;
			cout << endl;
		}

		// Close output file
		if (fclose(f_dump)) {
			printf("Could not close file '%s'\n", outPrint->dumpfile.c_str());
			exit(1);
		}
	}

	return;
}

void forwardFunctionDt(double* inpParams, double dTym, double* outValues) {
	// variables to store right hand side
	double dudt = 0.e0;
	double dvdt = 0.e0;
	double dwdt = 0.e0;

	// parse input parameters
	const double a = inpParams[0];
	const double b = inpParams[1];
	const double c = inpParams[2];

	// Save solution at current time step
	double u_o = outValues[0];
	double v_o = outValues[1];
	double w_o = outValues[2];

	// Integrate with 2nd order Runge Kutta

	// Compute right hand sides
	GetRHS(a, b, c, u_o, v_o, w_o, dudt, dvdt, dwdt);

	// Advance to mid-point
	double u = u_o + 0.5 * dTym * dudt;
	double v = v_o + 0.5 * dTym * dvdt;
	double w = w_o + 0.5 * dTym * dwdt;

	// Compute right hand sides
	GetRHS(a, b, c, u, v, w, dudt, dvdt, dwdt);

	// Advance to next time step
	u = u_o + dTym * dudt;
	v = v_o + dTym * dvdt;
	w = w_o + dTym * dwdt;

	// Store the output
	outValues[0] = u;
	outValues[1] = v;
	outValues[2] = w;

	return;
}

void GetRHS(const double& a, const double& b, const double & c, const double& u,
		const double& v, const double& w, double& dudt, double& dvdt,
		double& dwdt) {
	dudt = a * (v - u);
	dvdt = u * (b - w) - v;
	dwdt = u * v - c * w;

	return;
}

void GetRHS(const PCSet& aPCSet, const double* a, const double* b,
		const double* c, const double* u, const double* v, const double* w,
		double* dudt, double* dvdt, double* dwdt) {
	// Number of PC terms
	const int nPCTerms = aPCSet.GetNumberPCTerms();
	// Work variables
	double* dummy1 = new double[nPCTerms];
	double* dummy2 = new double[nPCTerms];

	// Build du/dt
	aPCSet.Subtract(v, u, dummy1);
	aPCSet.Prod(a, dummy1, dudt);

	// Build dv/dt
	aPCSet.Subtract(b, w, dummy1);
	aPCSet.MultiplyInPlace(dummy1, *u);
	aPCSet.Subtract(dummy1, v, dvdt);

	// Build dw/dt
	aPCSet.Prod(u, v, dummy1);
	aPCSet.Prod(c, w, dummy2);
	aPCSet.Subtract(dummy1, dummy2, dwdt);

	// Memory clean-up
	delete[] dummy1;
	delete[] dummy2;

	return;
}
