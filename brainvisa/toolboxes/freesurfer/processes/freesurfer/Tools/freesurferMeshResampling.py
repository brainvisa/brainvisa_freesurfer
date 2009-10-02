from neuroProcesses import *

name = '07 Mesh resampling'
userlevel = 2

signature = Signature(
  'PialMesh', ReadDiskItem('Pial', 'MESH mesh', enableConversion=0),
  'WhiteMesh', ReadDiskItem('White', 'MESH mesh'),
  'destination', ReadDiskItem('Ico Mesh', 'MESH mesh'),
  'Isin', ReadDiskItem('BaseFreesurferType', 'FreesurferIsin'),
  'ResampledPialMesh', WriteDiskItem('ResampledPial', 'MESH mesh'),
  'ResampledWhiteMesh', WriteDiskItem('ResampledWhite', 'MESH mesh'),
  )

def initialization(self):
  self.linkParameters('WhiteMesh', 'PialMesh')
  self.linkParameters('Isin', 'PialMesh')
  self.linkParameters('destination', 'PialMesh')
  self.linkParameters('ResampledPialMesh', 'PialMesh')
  self.linkParameters('ResampledWhiteMesh', 'PialMesh')

  
def execution(self, context):
  context.write('Resample brain mesh.')
  
  context.write('python -c \"from freesurfer.regularizeMeshFromIsin import regularizeMesh as f; f(\"%s\", \"%s\", \"%s\", \"%s\");\#'%(self.PialMesh.fullPath(), self.Isin.fullPath(), self.ResampledPialMesh.fullPath(), self.destination.fullPath()))
  context.system('python', '-c', 'from freesurfer.regularizeMeshFromIsin import regularizeMesh as f; f(\"%s\", \"%s\", \"%s\", \"%s\"); '%(self.PialMesh.fullPath(), self.Isin.fullPath(), self.ResampledPialMesh.fullPath(), self.destination.fullPath()))

  context.write('python -c \"from freesurfer.regularizeMeshFromIsin import regularizeMesh as f; f(\"%s\", \"%s\", \"%s\", \"%s\");\#'%(self.WhiteMesh.fullPath(), self.Isin.fullPath(), self.ResampledWhiteMesh.fullPath(), self.destination.fullPath()))
  context.system('python', '-c', 'from freesurfer.regularizeMeshFromIsin import regularizeMesh as f; f(\"%s\", \"%s\", \"%s\", \"%s\"); '%(self.WhiteMesh.fullPath(), self.Isin.fullPath(), self.ResampledWhiteMesh.fullPath(), self.destination.fullPath()))

  
