# Download OptimizationDataset from QCArchive
Download QM datasets from QCArchive (OptimizationDataset) and export data as HDF5 file.

## Description
- [directory]/`downloader-openff-default-opt-dataset.py` - Python script to download the QM dataset from QCArchive (OptimizationDataset).
- [directory]/`config.yaml` - Configuration file used to define what datasets to download from QCArchive.
- [directory]/`download.sh` - LSF job script to execute `downloader-openff-default.py`.
- [directory]/`check_status.py` - Python script to quickly check if the computation of each entry record from the QM dataset has successfully completed. This will return the following information.
    - Index number (zero indexing)
    - Status (Complete|Incomplete|INVALID)
    - Record name with the intial conformation ID
    - Record name without the intial conformation ID  
    - Number of snapshots from the optimization trajectory

## Basic Usage
- `gen2/`
    >bsub < download.sh

- `pepconf-dlc/`  
Since there were trouble connecting to the server at the time, subset of datasets that has completed successfully are downloaded and then merged into a single HDF5 file.
    >python check_status.py > logging.log  
    >grep_logging_complete.sh  
    >bsub < download.sh  

    Use `merge_hdf.ipynb` to merge HDF5 into a single file.
    
