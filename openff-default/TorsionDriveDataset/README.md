## Description
- `downloader-openff-default-torsion-dataset.py` - Python script to download the QM dataset from QCArchive (TorsionDriveDataset).
- [directory]/`config.yaml` - Configuration file used to define what datasets to download from QCArchive.
- [directory]/`download.sh` - LSF job script to execute `downloader-openff-default.py`.
- [directory]/`grab_status.py` - Python script to quickly check if the computation of each entry record from the QM dataset has successfully completed. This returns the following information.
    - Index number (zero indexing)
    - Status (Complete|Incomplete|INVALID)
    - Record name
    - Entry name without initial conformation ID

## Basic Usage
1. Move to one of the directories (e.g. `gen2/`).
2. Submit LSF job.
    >bsub < download.sh  
