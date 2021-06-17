#!/usr/bin/env python
"""
   Burak OZDAMAR
   Evry
   May 2021

usage:
python read_lammps.py <input_filename> <output_filename>
"""

import numpy as np
import os
import sys
from itertools import cycle

_, fname, out_fname = sys.argv

types = dict(zip([1, 2, 3, 4], ["H", "O", "N", "K"]))
atomtypes=[]

def process(lines):
    global atomtypes
    vector = read_aux_data(fname)[2]

    coords_raw = lines[9:]
    coords_raw = [line.strip().split(" ") for line in coords_raw]
    
    coords_and_types = np.array(coords_raw).astype(float)
    coords_and_types = coords_and_types[coords_and_types[:, 0].argsort()]  
    atomtypes_ = coords_and_types[:,2]
    atomtypes = [types.get(int(i), "S") for i in atomtypes_]
    
    coords = coords_and_types[:,4:] * vector 
    write_to_xyz(coords)


def write_to_xyz(coords, title = ' '):
    with open (out_fname, "a") as fout:
        fout.write("%d\n%s\n" % (coords.size / 3, title))
        for x, atomtype in zip(coords.reshape(-1, 3), cycle(atomtypes)):
            fout.write("%s %.8g %.8g %.8g\n" % (atomtype, x[0], x[1], x[2]))


def main(fname):
    if os.path.exists(out_fname):
        inp = input("Output file {} exists, do you want to overwrite it? (y/n) ".format(out_fname))
        if inp in ["y", "yes", "Y"]:
            os.remove(out_fname)
        else:
            print("Quitting!")
            sys.exit()
    lines = []
    n_atoms = read_aux_data(fname)[1]
    with open(fname) as f:
        for line in f:
            lines.append(line)
            if len(lines) == n_atoms + 9:
                process(lines)
                lines = []

def read_aux_data(fname):
    aux_data_raw = []
    with open(fname) as f:
        for line in f:
            aux_data_raw.append(line)
            if len(aux_data_raw) == 9:
                break
    aux_data = [line.strip() for line in aux_data_raw]
    n_atoms = int(aux_data[3])
    vector = [line.split(" ") for line in aux_data[5:8]]
    vector = np.array(vector).astype(float)[:,1]
    
    return aux_data, n_atoms, vector


if __name__ == "__main__":
    print("Input file: {}".format(fname))
    print("Output file: {}".format(out_fname))
    main(fname)
