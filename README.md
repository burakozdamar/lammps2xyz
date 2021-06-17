# lammps2xyz

Basic script to convert the output of LAMMPS to .xyz file to visualize in VMD

* If using without the topology file modify the keys & items of the 'types' dictionary.

./read_lammps.py <input_filename> <output_filename>


TODO:
* Implement argparse to receive atomic kinds from the command line.
* Make it work in tandem with the topology file.
