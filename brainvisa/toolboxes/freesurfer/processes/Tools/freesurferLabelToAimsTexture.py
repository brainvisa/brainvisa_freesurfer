from brainvisa.processes import *
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand
from glob import glob

name = '09/10 Converting freesurfer unreadable labels to aims textures.'
userlevel = 2

signature = Signature(
  'WhiteMesh', ReadDiskItem('White', 'MESH mesh', enableConversion=0),
  'Gyri', ReadDiskItem('FreesurferGyriTexture', 'FreesurferParcellation'),
  'SulciGyri', ReadDiskItem('FreesurferSulciGyriTexture', 'FreesurferParcellation'),
#  'Gyri', ReadDiskItem('FreesurferReadableGyriTexture', 'Series of FreesurferLabel'),
#  'SulciGyri', ReadDiskItem('FreesurferReadableSulciGyriTexture', 'Series of FreesurferLabel'),
  'GyriTexture', WriteDiskItem('FreesurferGyri', 'Texture'),
  'SulciGyriTexture', WriteDiskItem('FreesurferSulciGyri', 'Texture'),
  )

def initialization(self):
  self.linkParameters('Gyri', 'WhiteMesh')
  self.linkParameters('SulciGyri', 'WhiteMesh')
  self.linkParameters('GyriTexture', 'WhiteMesh')
  self.linkParameters('SulciGyriTexture', 'WhiteMesh')


def execution(self, context):
  context.write('Conversion of freesurfer labels to aims labels.')

  if self.Gyri.get('side')=='left':
    side = 'lh'
  elif self.Gyri.get('side')=='right':
    side = 'rh'
  else:
    context.write('Error in side')
    return


  launchFreesurferCommand(context,
                          self.Gyri.get('_database'),
                          'mri_annotation2label',
                          '--subject', self.Gyri.get('subject'),
                          '--hemi', side,
                          '--annotation', self.Gyri.fullName()[self.Gyri.fullName().rfind('/')+4:],
                          '--labelbase', self.Gyri.fullPath()[self.Gyri.fullPath().rfind('/')+1:])
  gyriFiles = sorted( glob( self.Gyri.fullPath() + '-*.label' ) )
  launchFreesurferCommand(context,
                          self.SulciGyri.get('_database'),
                          'mri_annotation2label',
                          '--subject', self.SulciGyri.get('subject'),
                          '--hemi', side,
                          '--annotation', self.SulciGyri.fullName()[self.SulciGyri.fullName().rfind('/')+4:],
                          '--labelbase', self.SulciGyri.fullPath()[self.SulciGyri.fullPath().rfind('/')+1:])
  sulciGyriFiles = sorted( glob( self.SulciGyri.fullPath() + '-*.label' ) )


  # GYRI PART
  context.write("---Gyri---")
  if gyriFiles:
    context.system('python', '-c', 'from freesurfer.freesurferTexture2Tex import freesurferTexture2TexBrainvisa as f; f(%s, \"%s\", \"%s\");'%(gyriFiles, self.WhiteMesh.fullPath(), self.GyriTexture.fullPath()))
  else:
    context.write("no gyri file, conversion from freesurfer failed")
  for i in gyriFiles:
    os.remove( i )
  
  # SULCI-GYRI PART
  context.write("---Sulci-Gyri---")
  if sulciGyriFiles:
    context.system('python', '-c', 'from freesurfer.freesurferTexture2Tex import freesurferTexture2TexBrainvisa as f; f(%s, \"%s\", \"%s\");'%(sulciGyriFiles, self.WhiteMesh.fullPath(), self.SulciGyriTexture.fullPath()))
  else:
    context.write("no sulci-gyri file, conversion from freesurfer failed")
  for i in sulciGyriFiles:
    os.remove( i )

 



