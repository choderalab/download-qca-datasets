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
#with open('config.yaml') as input:
#    config = yaml.safe_load(input.read())
subsets = ['SPICE PubChem Set 1 Single Points Dataset v1.2']

for subset in subsets:
    ds = client.get_collection('Dataset', subset)
    all_molecules = ds.get_molecules()
    for row in ds.list_records().iloc:
        spec = row.to_dict()
        if spec['method'] == 'b3lyp-d3bj':
            recs = ds.get_records(method=spec['method'], basis=spec['basis'], program=spec['program'], keywords=spec['keywords'])
            break
    logging.info('-------------------')

    names = []
    n_total_confs = 0
    for i in range(len(recs[0])):
        rec_d3bj  = recs[0].iloc[i].record
        rec_b3lyp = recs[1].iloc[i].record
        try:
            if rec_d3bj is not None and rec_b3lyp is not None and rec_d3bj.status == 'COMPLETE' and rec_b3lyp.status == 'COMPLETE':
                assert recs[0].index[i] == recs[1].index[i], print("#{}: index does not match".format(i))

                index = recs[0].index[i]
                name = index[:index.rfind('-')]
                names.append(name)
                logging.info("{:10d}\tCOMPLETE\t{}\t{}".format(i, index, name))
            else:
                logging.info("{:10d}\tINCOMPLETE\t{}".format(i, index))
        except:
            logging.info("{:10d}\tINVALID\t{}".format(i, recs[0].index[i]))
