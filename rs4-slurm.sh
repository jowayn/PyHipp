#!/bin/bash

# Submit this script with: sbatch <this-filename>

#SBATCH --time=24:00:00   # walltime
#SBATCH --ntasks=1   # number of processor cores (i.e. tasks)
#SBATCH --nodes=1   # number of nodes
#SBATCH --cpus-per-task=5      # number of processors per task
#SBATCH -J "rs4"   # job name

## /SBATCH -p general # partition (queue)
#SBATCH -o rs4-slurm.%N.%j.out # STDOUT
#SBATCH -e rs4-slurm.%N.%j.err # STDERR

# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE
python -u -c "import PyHipp as pyh; \
import DataProcessingTools as DPT; \
import os; \
import time; \
t0 = time.time(); \
print(time.localtime()); \
DPT.objects.processDirs(dirs=None, objtype=pyh.RPLSplit, channel=[*range(97,125)]); \
DPT.objects.processDirs(dirs=['sessioneye/array04','session01/array04'], cmd='import PyHipp as pyh; import DataProcessingTools as DPT; DPT.objects.processDirs(None, pyh.RPLLFP, saveLevel=1); DPT.objects.processDirs(None, pyh.RPLHighPass, saveLevel=1);'); \
os.chdir('session01/array04'); \
DPT.objects.processDirs(level='channel', cmd='import PyHipp as pyh; from PyHipp import mountain_batch; mountain_batch.mountain_batch(); from PyHipp import export_mountain_cells; export_mountain_cells.export_mountain_cells();'); \
print(time.localtime()); \
print(time.time()-t0);"

aws sns publish --topic-arn arn:aws:sns:ap-southeast-1:018084650241:awsnotify --message "RPLS4JobDone"
