from neuroProcesses import *
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand

name = '11 Resample label textures.'
userlevel = 2

signature = Signature(
  'WhiteMesh', ReadDiskItem('White', 'MESH mesh', enableConversion=0),
  'Isin', ReadDiskItem('BaseFreesurferType', 'FreesurferIsin'),
  'Gyri', ReadDiskItem('FreesurferGyri', 'Texture'),
  'SulciGyri', ReadDiskItem('FreesurferSulciGyri', 'Texture'),
  'ResampledGyri', WriteDiskItem('ResampledGyri', 'Texture'),
  'ResampledSulciGyri', WriteDiskItem('ResampledSulciGyri', 'Texture'),
  )

def initialization(self):
  self.linkParameters('Isin', 'WhiteMesh')
  self.linkParameters('Gyri', 'WhiteMesh')
  self.linkParameters('SulciGyri', 'WhiteMesh')
  self.linkParameters('ResampledGyri', 'WhiteMesh')
  self.linkParameters('ResampledSulciGyri', 'WhiteMesh')

  
def execution(self, context):
  context.write('Resample  brain mesh.')

  context.system('python', '-c', 'from freesurfer.regularizeParcelTexture import regularizeParcelTexture as f; f(\"%s\", \"%s\", \"%s\", \"%s\");'%(self.Isin.fullPath(), self.WhiteMesh.fullPath(), self.Gyri.fullPath(), self.ResampledGyri.fullPath()))

  context.system('python', '-c', 'from freesurfer.regularizeParcelTexture import regularizeParcelTexture as f; f(\"%s\", \"%s\", \"%s\", \"%s\");'%(self.Isin.fullPath(), self.WhiteMesh.fullPath(), self.SulciGyri.fullPath(), self.ResampledSulciGyri.fullPath()))

