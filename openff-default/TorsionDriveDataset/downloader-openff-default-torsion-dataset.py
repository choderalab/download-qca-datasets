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
outputfile = h5py.File('OPENFF-DEFAULT.hdf5', 'w')


recs_by_name = defaultdict(list)
smi_by_name = defaultdict(list)
for idx, subset in enumerate(config['subsets']):
    print(subset)
    ds = client.get_collection('TorsionDriveDataset', subset)
    record_names = list(ds.data.records)

    #for i, record_name in enumerate(record_names[:5]):
    for i, record_name in enumerate(record_names):
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
            
            #print(entry.name, name)
            recs_by_name[name].append(td_record)
            if smi_by_name[name] == []:
                smi_by_name[name].append(entry.attributes["canonical_isomeric_explicit_hydrogen_mapped_smiles"])
        else:
            print(i, record_name, td_record.status)


# Add the data to the HDF5 file
for name in recs_by_name:
    try:
        group_recs, group_xyz = [], []
        for td_record in recs_by_name[name]:
            for k, v in td_record.get_final_molecules().items():
                group_recs.append(td_record.get_final_results()[k])
                group_xyz.append(v.geometry)

        atomic_numbers = v.atomic_numbers   # grab atomic numbers from last molecule
        smiles = smi_by_name[name]
        qcvars = [{'total_energy': r.properties.return_energy, 'total_gradient': r.return_result} for r in group_recs]
        name = name.replace('/', '')  # Remove stereochemistry markers that h5py interprets as path separators

        group = outputfile.create_group(name)
        group.create_dataset('subset', data=[subset], dtype=h5py.string_dtype())
        group.create_dataset('smiles', data=[smiles], dtype=h5py.string_dtype())
        group.create_dataset("atomic_numbers", data=atomic_numbers, dtype=np.int16)
        ds = group.create_dataset('conformations', data=np.array(group_xyz), dtype=np.float32)
        ds.attrs['units'] = 'bohr'

        for key in qcvars[0].keys():
            dtype = np.float64 if 'energy' in key else np.float32
            ds = group.create_dataset(key, data=np.array([v[key] for v in qcvars], dtype=dtype), dtype=dtype)
            if key in units:
                ds.attrs['units'] = units[key]
    except:
        print(f"INVALID: {name}")
