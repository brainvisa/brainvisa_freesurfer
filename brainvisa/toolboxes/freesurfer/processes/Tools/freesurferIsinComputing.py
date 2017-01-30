import os, sys
from brainvisa.processes import *

name = 'Computation of resampling parameters'
userlevel = 2

signature = Signature(
  'SphereRegMesh', ReadDiskItem('SphereReg', 'Aims Mesh formats'),
  'destination', ReadDiskItem('Ico Mesh', 'GIFTI File'),
  'Isin', WriteDiskItem('BaseFreesurferType', 'FreesurferIsin'),
  )

def initialization(self):
  self.linkParameters('Isin', 'SphereRegMesh')
  self.linkParameters('destination', 'SphereRegMesh')

  
def execution(self, context):
  context.write('Conpute \'isin\' file, allowing the mesh resampling.')
  
  context.write('%s -c \"from freesurfer.regularizeSphericalMesh_hack4 import regularizeSphericalMesh as f; f(\'%s\', \'%s\', \'%s\');\"'%(os.path.basename(sys.executable), self.SphereRegMesh.fullPath(), self.Isin.fullPath(), self.destination.fullPath()))
    
  context.system('%s', '-c', 'from freesurfer.regularizeSphericalMesh_hack4 import regularizeSphericalMesh as f; f(\"%s\", \"%s\", \"%s\"); '%(os.path.basename(sys.executable), self.SphereRegMesh.fullPath(), self.Isin.fullPath(), self.destination.fullPath()))


