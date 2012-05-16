from brainvisa.processes import *
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand

name = '10 Converting freesurfer labels to Aims tex format.'
userlevel = 2

signature = Signature(
  'WhiteMesh', ReadDiskItem('White', 'MESH mesh', enableConversion=0),
  'Gyri', ReadDiskItem('FreesurferReadableGyriTexture', 'Series of FreesurferLabel'),
  'SulciGyri', ReadDiskItem('FreesurferReadableSulciGyriTexture', 'Series of FreesurferLabel'),
  'GyriTexture', WriteDiskItem('FreesurferGyri', 'Texture'),
  'SulciGyriTexture', WriteDiskItem('FreesurferSulciGyri', 'Texture'),
  )

def initialization(self):
  self.linkParameters('SulciGyri', 'WhiteMesh')
  self.linkParameters('Gyri', 'WhiteMesh')
  self.linkParameters('GyriTexture', 'WhiteMesh')
  self.linkParameters('SulciGyriTexture', 'WhiteMesh')

  
def execution(self, context):
  context.write('Resample brain mesh.')

  context.system('python', '-c', 'from freesurfer.freesurferTexture2Tex import freesurferTexture2TexBrainvisa as f; f(%s, \"%s\", \"%s\");'%(self.Gyri.fullPaths(), self.WhiteMesh.fullPath(), self.GyriTexture.fullPath()))

  context.system('python', '-c', 'from freesurfer.freesurferTexture2Tex import freesurferTexture2TexBrainvisa as f; f(%s, \"%s\", \"%s\");'%(self.SulciGyri.fullPaths(), self.WhiteMesh.fullPath(), self.SulciGyriTexture.fullPath()))

