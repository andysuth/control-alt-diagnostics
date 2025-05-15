#!/bin/bash

#SBATCH -C cpu
#SBATCH --qos=regular
#SBATCH --time=16:30:00
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=128
#SBATCH --cpus-per-task=2
#SBATCH -J <your job name, optional>

PREFILENAME= <e.g. Trojan_Horse_Sim_001>

export VSIMDIR=/global/cfs/cdirs/txsupp/vp13usrs/perlmutter/internal-gcc1230/vorpal-r43016/bin

source /global/cfs/cdirs/txsupp/vp13usrs/perlmutter/internal-gcc1230/vxsimall.sh
export TECHX_PRODUCT=VSim

srun --ntasks=1 --hint=nomultithread --ntasks-per-node=1 $VSIMDIR/txpp.py ./${PREFILENAME}.pre 
srun --hint=nomultithread --cpu_bind=cores $VSIMDIR/vorpal -i ./${PREFILENAME}.in -sd