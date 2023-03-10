#!/usr/bin/env python
# coding: utf-8
import os, sys
from qcportal import FractalClient
from collections import defaultdict
from rdkit import Chem
import numpy as np
import h5py
import yaml



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
outputfile = h5py.File('GEN2-OPTIMIZATION-DATASET-OPENFF-DEFAULT.hdf5', 'w')



for subset in config['subsets']:
    #output_basename = subset.replace(' ', '-')
    #outputfile = h5py.File(output_basename + '.hdf5', 'w')


    ds = client.get_collection('OptimizationDataset', subset)
    record_names = list(ds.data.records)
    

    recs_by_name = defaultdict(list)
    #mols_by_name = defaultdict(list)
    smi_by_name = defaultdict(list)   # get canonical_isomeric_explicit_hydrogen_mapped_smiles from entry because smiles are sometimes missing from molecule.extras
    #for i, record_name in enumerate(record_names[:5]):
    for i, record_name in enumerate(record_names):
        try:
            opt_record = ds.get_record(record_name, specification="default")  # OptimizationRecord
            if opt_record is not None and opt_record.status == 'COMPLETE':
                entry = ds.get_entry(record_name)
                name = entry.name[:entry.name.rfind('-')]
                recs_by_name[name].append(opt_record)
                if smi_by_name[name] == []:
                    smi_by_name[name].append(entry.attributes["canonical_isomeric_explicit_hydrogen_mapped_smiles"])
            else:
                print(i, record_name, opt_record.status)
        except:
            print("invalid record name: {}".format(record_name))


    # Add the data to the HDF5 file.
    for name in recs_by_name:
        group_recs = []
        for opt_record in recs_by_name[name]:
            group_recs += [ record for record in opt_record.get_trajectory() ]        
        molecule = recs_by_name[name][0].get_initial_molecule()
        smiles = smi_by_name[name]
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