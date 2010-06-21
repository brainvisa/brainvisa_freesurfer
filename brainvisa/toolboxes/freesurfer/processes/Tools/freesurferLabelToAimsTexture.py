from neuroProcesses import *
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand

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

  launchFreesurferCommand(context,
                          self.SulciGyri.get('_database'),
                          'mri_annotation2label',
                          '--subject', self.SulciGyri.get('subject'),
                          '--hemi', side,
                          '--annotation', self.SulciGyri.fullName()[self.SulciGyri.fullName().rfind('/')+4:],
                          '--labelbase', self.SulciGyri.fullPath()[self.SulciGyri.fullPath().rfind('/')+1:])


  # DATABASE UPDATE

  context.write("Clearing database...")
  neuroHierarchy.databases.clear()
  context.write("Database cleared")
  context.write("Updating database...")
  neuroHierarchy.databases.update()
  context.write("database updated")
  #f = neuroHierarchy.databases.findDiskItem(_type='FreesurferParcellationPath', subject=self.WhiteMesh.get('subject'))
  #context.write("Updating database, path = " + f.fullPath())
  #neuroHierarchy.databases.update([f.fullPath()])
  #context.write("database updated, path = " + f.fullPath())

  # GYRI PART
  context.write("---Gyri---")
  f = neuroHierarchy.databases.findDiskItem(_type='FreesurferReadableGyriTexture', subject=self.WhiteMesh.get('subject'), side=self.WhiteMesh.get('side'))
  if f!=None:
    context.write("Gyri part, read file = " + f.fullPath())
    context.system('python', '-c', 'from freesurfer.freesurferTexture2Tex import freesurferTexture2TexBrainvisa as f; f(%s, \"%s\", \"%s\");'%(f.fullPaths(), self.WhiteMesh.fullPath(), self.GyriTexture.fullPath()))
  else:
    context.write("no gyri file, conversion from freesurfer failed")

  # SULCI-GYRI PART
  context.write("---Sulci-Gyri---")
  f = neuroHierarchy.databases.findDiskItem(_type='FreesurferReadableSulciGyriTexture', subject=self.WhiteMesh.get('subject'), side=self.WhiteMesh.get('side'))
  if f!=None:
    context.write("Sulci-Gyri part, read file = " + f.fullPath())
    context.system('python', '-c', 'from freesurfer.freesurferTexture2Tex import freesurferTexture2TexBrainvisa as f; f(%s, \"%s\", \"%s\");'%(f.fullPaths(), self.WhiteMesh.fullPath(), self.SulciGyriTexture.fullPath()))
  else:
    context.write("no sulci-gyri file, conversion from freesurfer failed")

 



