# first argument cluster name
# second argument key name
# third argument snapshot tag
# fourth argument snapshot count

if [ "$#" -lt 2 ];
then
	echo "at least 2 arguments required - cluster name, key name"
	exit
fi

curr_ip=$(curl -s ifconfig.co)
target_ip=$(pcluster status $1 | grep PublicIP: | cut -d " " -f 2)
echo current base ip address: $curr_ip
echo master node ip address: $target_ip
scp -o StrictHostKeyChecking=no -i $2 $2 ec2-user@$target_ip:~/
if (($? > 0));
then
	echo key transfer failed, possibly due to read-only same-name key at target location or bad cluster name
	exit
fi
fullpath=$2
echo "#!/bin/sh" > shutdown_cluster.sh
echo "ssh -o StrictHostKeyChecking=no -t -i ~/${fullpath##*/} ec2-user@$curr_ip 'source ~/.bash_profile && touch left_cluster.note && sh update_snapshot.sh $3 $4 $1 && touch snapshot_saved.note && pcluster delete $1 && touch cluster_deleted.note'" >> shutdown_cluster.sh
scp -o StrictHostKeyChecking=no -i $2 shutdown_cluster.sh ec2-user@$target_ip:~/
rm shutdown_cluster.sh
scp -o StrictHostKeyChecking=no -i $2 consol_jobs.sh ec2-user@$target_ip:~/
