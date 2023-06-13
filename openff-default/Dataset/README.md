# Download BasicDataset from QCArchive
Download QM datasets from QCArchive (BasicDataset) and export data as HDF5 file.

## Description
- `downloader-openff-default.py` - Python script to download the QM dataset from QCArchive.
- [directory]/`config.yaml` - Configuration file used to define what datasets to download from QCArchive.
- [directory]/`download.sh` - LSF job script to execute `downloader-openff-default.py`.
- [directory]/`check_status.py` - Python script to quickly check if the computation of each entry record from the QM dataset has successfully completed. This will return the following information.
    - Index number (zero indexing)
    - Status (Complete|Incomplete|INVALID)
    - Record name with conformation ID
    - Record name without conformation ID  

## Basic Usage
1. Move to one of the directories (e.g. rna-nucleoside).
2. Submit lsf job.
    >bsub < download.sh  

## Notes
- `rna-diverse` ([RNA Single Point Dataset v1.0](https://github.com/openforcefield/qca-dataset-submission/tree/master/submissions/2022-07-07-RNA-basepair-triplebase-single-points)) stores single point energy calculations of intermolecular RNA base pairs and base triples and connected trinucleotides. In this study, only the trinucleotides are extracted from the QCArchive dataset.
