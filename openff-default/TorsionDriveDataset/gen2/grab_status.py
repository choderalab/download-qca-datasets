#!/usr/bin/env python
# coding: utf-8
import os, sys
from qcportal import FractalClient
from collections import defaultdict
from rdkit import Chem
import numpy as np
import h5py
import yaml
import logging
logging.basicConfig(filename='logging.log', encoding='utf-8', level=logging.INFO)


client = FractalClient()
with open('config.yaml') as input:
    config = yaml.safe_load(input.read())


for subset in config['subsets']:
    ds = client.get_collection('TorsionDriveDataset', subset)
    record_names = list(ds.data.records)

    for i, record_name in enumerate(record_names):
        #try:
        td_record = ds.get_record(record_name, specification="default")
        assert td_record.qc_spec.method == 'b3lyp-d3bj'

        if td_record is not None and td_record.status == 'COMPLETE':
            entry = ds.get_entry(record_name)
            #name = index[:index.rfind('-')]  # This does not work for TorsionDriveDataset

            # Note: "-" is attached to entry names to discriminate different initial structures.
            # entry.name.rfind('-') will try to find the last index with "-" but will return -1 if "-" is not present in the entry name. 
            # This will slice the last letter from the entry name and could interpret different molecules as a same molecule because the 
            # entry names are truncated. Here, we assume that initial structures for each molecule is less than 10.
            index = entry.name.rfind('-')
            
            # ensure the letters after the slice is something like "-X"
            if len(entry.name[index:]) == 2:
                name = entry.name[:index]
            else:
                name = entry.name
            logging.info("{:10d}\tCOMPLETE\t{}\t{}".format(i, record_name, name))
        else:
            logging.info("{:10d}\tINCOMPLETE\t{}".format(i, record_name))
        #except:
        #    logging.info("{:10d}\tINVALID\t{}".format(i, record_name))
