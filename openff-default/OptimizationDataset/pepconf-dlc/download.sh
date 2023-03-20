#!/bin/bash
#BSUB -P "pepconf"
#BSUB -J "pepconf"
#BSUB -n 1
###BSUB -R rusage[mem=64]
#BSUB -R rusage[mem=128]
#BSUB -R span[hosts=1]
#BSUB -q cpuqueue
#BSUB -sp 1 # low priority. default is 12, max is 25
#BSUB -W 23:00
#BSUB -o out_%J_%I.stdout
#BSUB -eo out_%J_%I.stderr
#BSUB -L /bin/bash


source ~/.bashrc


# change dir
echo "changing directory to ${LS_SUBCWD}"
cd $LS_SUBCWD

conda activate espaloma

# ----
# DOWNLOAD SUBSET OF DATA TO AVOID LSF MEMORY LIMIT
# ----

#echo 'download entries 0 to 1000'
#/bin/time --verbose python downloader-openff-default-opt-dataset-revised-dlc.py 0    1000 "OpenFF-PEPCONF-OptimizationDataset-part1.hdf5"
#sleep 60

#echo 'download entries 1000 to 2000'
#/bin/time --verbose python downloader-openff-default-opt-dataset-revised-dlc.py 1000 2000 "OpenFF-PEPCONF-OptimizationDataset-part2.hdf5"
#sleep 60

#echo 'download entries 2000 to 2500'
#/bin/time --verbose python downloader-openff-default-opt-dataset-revised-dlc.py 2000 2500 "OpenFF-PEPCONF-OptimizationDataset-part3.hdf5"
#sleep 60

#echo 'download entries 2500 to 3000'
#/bin/time --verbose python downloader-openff-default-opt-dataset-revised-dlc.py 2500 3000 "OpenFF-PEPCONF-OptimizationDataset-part4.hdf5"
#sleep 60

#echo 'download entries 3000 to 3500'
#/bin/time --verbose python downloader-openff-default-opt-dataset-revised-dlc.py 3000 3500 "OpenFF-PEPCONF-OptimizationDataset-part5.hdf5"
#sleep 60

echo 'download entries 3500 to last'
/bin/time --verbose python downloader-openff-default-opt-dataset-revised-dlc.py 3500 9999 "OpenFF-PEPCONF-OptimizationDataset-part6.hdf5"
sleep 60

echo done