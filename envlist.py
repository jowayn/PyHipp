#!/data/miniconda3/envs/env1/bin/python

from filelock import FileLock
import hickle
import sys

# set constants
file_path = "/data/picasso/envlist.hkl"
lock_path = "/data/picasso/envlist.khl.lock"
time_out_secs = 60

# program modes
READ_MODE = 0
WRITE_MODE = 1
RESET_MODE = 2

# get number of arguments
nargs = len(sys.argv)
if nargs > 3:
    print('Usage: envlist; envlist env; envlist envprefix nenvs')
    exit
elif nargs > 2:
    # creates or re-creates the list of environments
    pmode = RESET_MODE
    # get prefix for environment name
    envprefix = sys.argv[1]
    # get number of environments to create
    nenvs = sys.argv[2]
elif nargs > 1:
    # returns env to the list of environments
    pmode = WRITE_MODE
    # get name of environment to return
    env = sys.argv[1]
else:
    # gets name of an environment to use
    pmode = READ_MODE

# creates a lock for the file so it can only be accessed one at a time
lock = FileLock(lock_path, timeout=time_out_secs)

with lock:
    if pmode == RESET_MODE:
        # create a list (named clist) of nevns environments with the 
        # prefix envprefix
<<<<<<< HEAD
        clist = [f"{envprefix}{i}" for i in range(int(nenvs))]
=======
        clist1 = [*range(0,int(nenvs),1)]
        clist = [envprefix + str(s) for s in clist1]
>>>>>>> upstream/main
    else:
        # load hickle file
        clist = hickle.load(file_path)

        if pmode == WRITE_MODE:
            # append item to end of list
            clist.append(env)
<<<<<<< HEAD
        else:    
=======
        else:
>>>>>>> upstream/main
            # get and remove env from clist
            env = clist.pop(0)
            # return env name
            print(env)

    # save hickle file
    hickle.dump(clist, file_path, mode="w")
