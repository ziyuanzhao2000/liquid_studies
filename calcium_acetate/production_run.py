# NVT production run, E field at 1MV/cm

from mdtools import MDSystem
from simtk.unit import *
from simtk.openmm.app import PDBFile

input = 'post_NPT.pdb'
field_strength = 1e8 # V/m
pdbfile = PDBFile('post_NPT.pdb')
mdsystem = MDSystem(pdbfile.topology, pdbfile.positions, forcefield)
mdsystem.buildSimulation(filePrefix=f"NVT_EF_run", ensemble='NVT',
                         efx=True, ef=(field_strength, 0, 0),
                         saveTrajectory=True, trajInterval=500, saveVelocities=True,
                         saveStateData=True, stateDataInterval=500)
mdsystem.simulate(1000*picoseconds)
mdsystem.save('NVT_EF_run.pdb')