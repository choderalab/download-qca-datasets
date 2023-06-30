## Description
- [directory]/`downloader-openff-default-opt-dataset.py` - Python script to download the QM dataset from QCArchive (OptimizationDataset).
- [directory]/`config.yaml` - Configuration file used to define what datasets to download from QCArchive.
- [directory]/`download.sh` - LSF job script to execute `downloader-openff-default.py`.
- [directory]/`check_status.py` - Python script to quickly check if the computation of each entry record from the QM dataset has successfully completed. This returns the following information.
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

    `merge_hdf.ipynb` was used to merge the HDF5 files into a single file.
    
