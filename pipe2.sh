#!/bin/bash

# first job called from the day directory
# creates RPLParallel, Unity, and EDFSplit objects, and
# calls aligning_objects and raycast
sbatch /data/src/PyHipp/rplparallel-slurm.sh

# second set of jobs called from the day directory
sbatch /data/src/PyHipp/rs1-slurm.sh
sbatch /data/src/PyHipp/rs2-slurm.sh
sbatch /data/src/PyHipp/rs3-slurm.sh
sbatch /data/src/PyHipp/rs4-slurm.sh

