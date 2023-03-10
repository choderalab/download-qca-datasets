#!/usr/bin/env python
# coding: utf-8
import os, sys
from qcportal import FractalClient
from collections import defaultdict
from rdkit import Chem
import numpy as np
import h5py
import yaml


"""
Note: Only 1805/7560 record entries were completed. Extract completed record entries from logging information. 
"""


INDEX_START = int(sys.argv[1])
INDEX_END = int(sys.argv[2])
OUTPUT_FILENAME = str(sys.argv[3])


# Units for a variety of fields that can be downloaded.
units = {'total_energy': 'hartree',
         'total_gradient': 'hartree/bohr'}


# Process the configuration file and download data.
with open('config.yaml') as input:
    config = yaml.safe_load(input.read())
if 'max_force' in config:
    max_force = float(config['max_force'])
else:
    max_force = None
client = FractalClient()
outputfile = h5py.File(OUTPUT_FILENAME, 'w')


for subset in config['subsets']:
    ds = client.get_collection('OptimizationDataset', subset)
    #record_names = list(ds.data.records)
    #n_records = len(ds.data.records)
    
    x = ds.status(["default"])
    N_MAX = int(x['default']['COMPLETE'])
    if INDEX_END > N_MAX:
        INDEX_END = N_MAX
        print('INDEX_END is set to {}'.format(N_MAX))

    # Get record_names that successfully completed QM calculation
    record_names= []
    with open("logging_complete.log", "r") as f:
        for l in f.readlines()[INDEX_START:INDEX_END]:
            l = l.split()
            status = l[2]
            if status.startswith('COMPLETE'):
                record_name = l[3]
                record_names.append(record_name)

    # All record entries should be completed since we are grabbing 
    # only successful entries based on logging information
    recs_by_name = defaultdict(list)
    for i, record_name in enumerate(record_names):
        opt_record = ds.get_record(record_name, specification="default")
        entry = ds.get_entry(record_name)
        name = entry.name[:entry.name.rfind('-')]
        recs_by_name[name].append(opt_record)
    

    # Add the data to the HDF5 file.
    for name in recs_by_name:
        group_recs = []
        for opt_record in recs_by_name[name]:
            group_recs += [ record for record in opt_record.get_trajectory() ]        
        molecule = recs_by_name[name][0].get_initial_molecule()
        smiles = molecule.extras['canonical_isomeric_explicit_hydrogen_mapped_smiles']
        qcvars = [{'total_energy': r.properties.return_energy, 'total_gradient': r.return_result} for r in group_recs]
        name = name.replace('/', '')  # Remove stereochemistry markers that h5py interprets as path separators

        group = outputfile.create_group(name)
        group.create_dataset('subset', data=[subset], dtype=h5py.string_dtype())
        group.create_dataset('smiles', data=[smiles], dtype=h5py.string_dtype())
        group.create_dataset("atomic_numbers", data=molecule.atomic_numbers, dtype=np.int16)

        # conformations
        ds = group.create_dataset('conformations', data=np.array([rec.get_molecule().geometry for rec in group_recs]), dtype=np.float32)
        ds.attrs['units'] = 'bohr'
        
        for key in qcvars[0].keys():
            dtype = np.float64 if 'energy' in key else np.float32
            ds = group.create_dataset(key, data=np.array([v[key] for v in qcvars], dtype=dtype), dtype=dtype)
            #ds = group.create_dataset(key, data=np.array([v[key] for v in qcvars], dtype=np.float64), dtype=np.float64)
            if key in units:
                ds.attrs['units'] = units[key]
