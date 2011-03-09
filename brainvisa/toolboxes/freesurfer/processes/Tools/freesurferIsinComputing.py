from neuroProcesses import *

name = '06 Computation of resampling parameters'
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
  
  context.write('python -c \"from freesurfer.regularizeSphericalMesh_hack4 import regularizeSphericalMesh as f; f(\'%s\', \'%s\', \'%s\');\"'%(self.SphereRegMesh.fullPath(), self.Isin.fullPath(), self.destination.fullPath()))
    
  context.system('python', '-c', 'from freesurfer.regularizeSphericalMesh_hack4 import regularizeSphericalMesh as f; f(\"%s\", \"%s\", \"%s\"); '%(self.SphereRegMesh.fullPath(), self.Isin.fullPath(), self.destination.fullPath()))


