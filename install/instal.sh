#/bin/sh
#SET TO CORRECT PYTHON PATH
export PYTHONPATH=${PYTHONPATH}:../lib/
#export PYTHONPATH=../lib/

#INSTALL NUMPY
#cd ./numpy
#python setup.py install --prefix=../../lib
#cd ..

#INSTALL MATPLOTLIB
cd ./matplotlib
python setup.py install --prefix=../../lib
cd ..
