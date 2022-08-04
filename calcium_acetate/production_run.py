# NVT production run, E field at 1MV/cm

# Create an OpenFF Molecule object for benzene from SMILES
from openff.toolkit.topology import Molecule
molecule = Molecule.from_smiles('CC(=O)[O-]')

# Create the GAFF template generator
from openmmforcefields.generators import GAFFTemplateGenerator
gaff = GAFFTemplateGenerator(molecules=molecule)

# Create an OpenMM ForceField object with AMBER ff14SB and TIP3P with compatible ions
from simtk.openmm.app import ForceField
forcefield = ForceField('amber/ff14SB.xml', 'amber/tip3p_standard.xml')

# Register the GAFF template generator
forcefield.registerTemplateGenerator(gaff.generator)

from mdtools import MDSystem
from simtk.unit import *
from simtk.openmm.app import PDBFile

input = 'post_NPT.pdb'
field_strength = 1e8 * volts/meters # V/m
pdbfile = PDBFile(input)
mdsystem = MDSystem(pdbfile.topology, pdbfile.positions, forcefield)
mdsystem.buildSimulation(filePrefix=f"NVT_EF_run", ensemble='NVT',
                         efx=True, ef=(field_strength, 0, 0),
                         saveTrajectory=True, trajInterval=500, saveVelocities=True,
                         saveStateData=True, stateDataInterval=500)
mdsystem.simulate(1000*picoseconds)
mdsystem.save('NVT_EF_run.pdb')
