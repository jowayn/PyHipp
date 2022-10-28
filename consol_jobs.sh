#!/bin/sh

temp1=($(squeue))

cmd1="sbatch --dependency=afterany:"

counter1=0
for i in "${temp1[@]}"; do
       if [[ "$i" == "queue1" ]]; then
	       id1=${temp1[$counter1-1]}
	       cmd1="${cmd1}${id1}:"
       fi
       counter1=$((counter1+1))
done

cmd1=${cmd1::-1}
cmd1="${cmd1} /data/src/PyHipp/ec2snapshot.sh"

echo $cmd1
eval $cmd1
