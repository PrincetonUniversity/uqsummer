make
./lorenzNISP.x
mv solution.dat solution_NISP.dat 
./lorenzISP.x 
mv solution.dat solution_ISP.dat 
./pllorenzMstd.py NISP
./pllorenzMstd.py ISP

