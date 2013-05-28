
struct postAux
     {
       Array2D<double> data;
       Array1D<double> modelparams;
       Array1D<string> modelparamnames;
       Array1D<double> modelauxparams;
       Array1D<double> postparams;
       string noisetype;
       Array1D<string> priortype;
       Array1D<double> priorparam1;
       Array1D<double> priorparam2;
       Array1D<int> chainParamInd;
 }; 



/// \brief Evaluate the log of the posterior for a given set of model
  /// and nuisance parameters
  double LogPosterior(Array1D<double>& m, void *info);



double LogPosterior(Array1D<double>& m, void *info)
{
  double pi=4.*atan(1.);

  postAux* pinfo = (postAux*) info;

  double logprior=0;
  
  for(int ic=0;ic<m.Length();ic++){

    if(!strcmp(pinfo->priortype(ic).c_str(),"uniform")){
      double a=pinfo->priorparam1(ic);
      double b=pinfo->priorparam2(ic);
      if (a>=b)
	throw Tantrum("Prior bounds are incorrect!");
    logprior -= log(b-a);
    }

    else if(!strcmp(pinfo->priortype(ic).c_str(),"normal")){
      double mu=pinfo->priorparam1(ic);
      double sig=pinfo->priorparam2(ic);
    
      logprior -= 0.5*log(2.*pi*sig*sig);
      logprior -= 0.5*pow((m(ic)-mu)/sig,2.0);
    }
    else
      throw Tantrum("Only unifrom or normal priors are implemented!");
  }


     Array2D<double> data=pinfo->data;
     Array1D<double> modelparams=pinfo->modelparams;
     // Set the parameter values for the forward run
     int chaindim=m.XSize();
     for(int ic=0;ic<chaindim;ic++)
       modelparams(pinfo->chainParamInd(ic))=m(ic);

  // Posterior parameter 
     // Either Proportionaility constant between signal and noise for likelihood construction
     // or standard deviation itself
     double stdpar=pinfo->postparams(0);


  // Time and time step
  double t0 = 0.0;
  double tf = pinfo->modelauxparams(0);
  double dTym = pinfo->modelauxparams(1);

  // Initial conditions of zero coverage (based on Makeev:2002)
  double u = 0.e0;
  double v = 0.e0;
  double w = 0.e0;
  double outValues[]={u,v,w};
  
  // Forward ODE function
  dumpInfo* outprint = 0;
  forwardFunction(modelparams.GetArrayPointer(), t0, tf, dTym, outValues,outprint);

 // Get the output of interest to compare with data
 // Only assume we have data on variables u and v
 double umodel=outValues[0]; 
 double vmodel=outValues[1];
 
 // Compare the model data with measurement data according to the noise model
 // to get the likelihood.
 double std1;
 double std2;
 if(!strcmp(pinfo->noisetype.c_str(),"const_stn")){
   std1=stdpar*umodel;
   std2=stdpar*vmodel;
 }
 else    if(!strcmp(pinfo->noisetype.c_str(),"const_stdev")){
   std1=stdpar;
   std2=stdpar;
 }
 else
   throw Tantrum("Noise type is not recognized!");
 
 double var1=std1*std1;
 double var2=std2*std2;
 double sum=logprior;
 int nTot=data.XSize();
 for(int it=0; it < nTot; it++){
   
   double err1=data(it,0)-umodel;
   double err2=data(it,1)-vmodel;
   sum  = sum - log(2*pi) - 0.5*log(var1) - 0.5*log(var2) - pow(err1,2)/(2.0*var1) - pow(err2,2)/(2.0*var2);
 
}

 

 return sum;
 
}
