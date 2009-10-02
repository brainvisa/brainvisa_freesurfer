from neuroProcesses import *

name = '05 Conversion of Gifti meshes to Aims mesh format'
userlevel = 2

signature = Signature(
  'PialGifti', ReadDiskItem('Pial', 'GIFTI File'),
  'WhiteGifti', ReadDiskItem('White', 'GIFTI File'),
  'SphereRegGifti', ReadDiskItem('SphereReg', 'GIFTI File'),
  'PialMesh', WriteDiskItem('Pial', 'MESH mesh'),
  'WhiteMesh', WriteDiskItem('White', 'MESH mesh'),
  'SphereRegMesh', WriteDiskItem('SphereReg', 'MESH mesh'),
  )

def initialization(self):
  self.linkParameters('WhiteGifti', 'PialGifti')
  self.linkParameters('SphereRegGifti', 'PialGifti')
  self.linkParameters('PialMesh', 'PialGifti')
  self.linkParameters('WhiteMesh', 'PialGifti')
  self.linkParameters('SphereRegMesh', 'PialGifti')
  
def execution(self, context):
  context.write('Convert meshes in Gifti fromat to Aims mesh format.')
  
  # Pial
  context.write('python -c \"from freesurfer.GiftiToBrainvisa import GiftiToBrainvisa as f; f(\'%s\', \'%s\');\"'%(self.PialGifti.fullPath(), self.PialMesh.fullPath()))
  context.system('python', '-c', 'from freesurfer.GiftiToBrainvisa import GiftiToBrainvisa as f; f(\"%s\", \"%s\"); '%(self.PialGifti.fullPath(), self.PialMesh.fullPath()))
  
  # White
  context.write('python -c \"from freesurfer.GiftiToBrainvisa import GiftiToBrainvisa as f; f(\'%s\', \'%s\');\"'%(self.WhiteGifti.fullPath(), self.WhiteMesh.fullPath()))
  context.system('python', '-c', 'from freesurfer.GiftiToBrainvisa import GiftiToBrainvisa as f; f(\"%s\", \"%s\"); '%(self.WhiteGifti.fullPath(), self.WhiteMesh.fullPath()))
  
  # SphereReg
  context.write('python -c \"from freesurfer.GiftiToBrainvisa import GiftiToBrainvisa as f; f(\'%s\', \'%s\');\"'%(self.SphereRegGifti.fullPath(), self.SphereRegMesh.fullPath()))
  context.system('python', '-c', 'from freesurfer.GiftiToBrainvisa import GiftiToBrainvisa as f; f(\"%s\", \"%s\"); '%(self.SphereRegGifti.fullPath(), self.SphereRegMesh.fullPath()))
