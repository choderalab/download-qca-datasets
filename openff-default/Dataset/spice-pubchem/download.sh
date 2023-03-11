#!/bin/bash
#BSUB -P "spice"
#BSUB -J "spice-dl"
#BSUB -n 1
#BSUB -R rusage[mem=64]
#BSUB -R span[hosts=1]
#BSUB -q cpuqueue
#BSUB -sp 1 # low priority. default is 12, max is 25
#BSUB -W 12:00
#BSUB -o out_%J_%I.stdout
#BSUB -eo out_%J_%I.stderr
#BSUB -L /bin/bash


source ~/.bashrc


# change dir
echo "changing directory to ${LS_SUBCWD}"
cd $LS_SUBCWD

conda activate espaloma
/bin/time --verbose python downloader-openff-default.py
echo done

mv OPENFF-DEFAULT.hdf5 SPICE-PUBCHEM-OPENFF-DEFAULT.hdf5