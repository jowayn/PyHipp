#!/bin/bash

find . -name "*.hkl" -or -name "*.csv" | xargs rm

find . -name "*slurm*err" -or -name "*slurm*out" | xargs rm

rm -r mountains

cd session01

rm binData.hdf logs.txt slist.txt VirtualMaze*

cd ..

