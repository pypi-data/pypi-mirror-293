#!/bin/bash 
#SBATCH --partition bansil
#SBATCH --nodes     2
#SBATCH --ntasks    128
#SBATCH --job-name  remote_UTe3
#SBATCH --output    remote_UTe3.out


export PATH="/work/bansil/s.sevim/software/qe-7.3/q-e/bin/:$PATH"
source /shared/centos7/intel/oneapi/2022.1.0/setvars.sh
source /work/bansil/s.sevim/remote-deploy/espresso-machine/.venv/bin/activate
python3 job_UTe3.py
