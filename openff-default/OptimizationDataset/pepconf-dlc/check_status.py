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
subsets = ['OpenFF PEPCONF OptimizationDataset v1.0']

for subset in subsets:
    ds = client.get_collection('OptimizationDataset', subset)
    logging.info(ds.status(["default-dlc"]))
    logging.info('-------------------')

    record_names = list(ds.data.records)
    logging.info(">   {}".format(subset))

    names = []
    n_total_confs = 0
    for i, record_name in enumerate(record_names):
        try:
            opt_record = ds.get_record(record_name, specification="default-dlc")  # OptimizationRecord
            if opt_record is not None and opt_record.status == 'COMPLETE':
                n_confs = len(opt_record.energies)
                n_total_confs += n_confs
                
                entry = ds.get_entry(record_name)
                name = entry.name[:entry.name.rfind('-')]
                names.append(name)
                logging.info("{:10d}\tCOMPLETE\t{}\t{}\t{}".format(i, record_name, name, n_confs))
            else:
                logging.info("{:10d}\tINCOMPLETE\t{}".format(i, record_name))
        except:
            logging.info("{:10d}\tINVALID\t{}".format(i, record_name))

    logging.info('-------------------')
    logging.info("{} records found".format(len(record_names)))
    logging.info("{} entries completed".format(len(names)))
    logging.info("{} unique mols completed".format(len(set(names))))
    logging.info("{} total conformations".format(n_total_confs))
    logging.info("\n\n")
    
