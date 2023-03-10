#!/bin/bash
#BSUB -P "pepconf"
#BSUB -J "pepconf"
#BSUB -n 1
##BSUB -R rusage[mem=12]
#BSUB -R rusage[mem=64]
#BSUB -R span[hosts=1]
#BSUB -q cpuqueue
#BSUB -sp 1 # low priority. default is 12, max is 25
#BSUB -W 36:00
#BSUB -o out_%J_%I.stdout
#BSUB -eo out_%J_%I.stderr
#BSUB -L /bin/bash


source ~/.bashrc


# change dir
echo "changing directory to ${LS_SUBCWD}"
cd $LS_SUBCWD

conda activate espaloma

echo 'download entries 0 to 500'
/bin/time --verbose python downloader-openff-default-opt-dataset-revised.py 0     500 "OpenFF-PEPCONF-OptimizationDataset-part1.hdf5"
sleep 60

echo 'download entries 500 to 1000'
/bin/time --verbose python downloader-openff-default-opt-dataset-revised.py 500  1000 "OpenFF-PEPCONF-OptimizationDataset-part2.hdf5"
sleep 60

echo 'download entries 1000 to 1500'
/bin/time --verbose python downloader-openff-default-opt-dataset-revised.py 1000 1500 "OpenFF-PEPCONF-OptimizationDataset-part3.hdf5"
sleep 60

echo 'download entries 1500 to last'
/bin/time --verbose python downloader-openff-default-opt-dataset-revised.py 1500 9999 "OpenFF-PEPCONF-OptimizationDataset-part4.hdf5"
sleep 60

echo done