#!/bin/bash

# Submit this script with: sbatch <this-filename>

#SBATCH --time=24:00:00   # walltime
#SBATCH --ntasks=1   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
<<<<<<< HEAD
#SBATCH --cpus-per-task=1   # number of CPUs for this task
=======
#SBATCH --cpus-per-task=1	# number of processors per task
>>>>>>> upstream/main
#SBATCH -J "rse"   # job name

## /SBATCH -p general # partition (queue)
#SBATCH -o rse-slurm.%N.%j.out # STDOUT
#SBATCH -e rse-slurm.%N.%j.err # STDERR

# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE
<<<<<<< HEAD

python -u -c "import PyHipp as pyh; \
import time; \
import os; \
=======
python -u -c "import PyHipp as pyh; \
import os; \
import time; \
>>>>>>> upstream/main
t0 = time.time(); \
print(time.localtime()); \
os.chdir('sessioneye'); \
pyh.RPLSplit(SkipLFP=False, SkipHighPass=False); \
print(time.localtime()); \
print(time.time()-t0);"
<<<<<<< HEAD
=======

aws sns publish --topic-arn arn:aws:sns:ap-southeast-1:018084650241:awsnotify --message "RSEJobDone"
>>>>>>> upstream/main
