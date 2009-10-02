from neuroProcesses import *
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand

name = '09 Converting labels to readable ascii format.'
userlevel = 2

signature = Signature(
  'Gyri', ReadDiskItem('FreesurferGyriTexture', 'FreesurferParcellation'),
  'SulciGyri', ReadDiskItem('FreesurferSulciGyriTexture', 'FreesurferParcellation'),
  )

def initialization(self):
  self.linkParameters('SulciGyri', 'Gyri')

  
def execution(self, context):
  context.write('Resample brain mesh.')
  #context.write(neuroHierarchy.databases.findDiskItem(_type='FreesurferParcellationPath', subject='s12069'))
  #neuroHierarchy.databases.update(['/volatile/alan/freesurfertest/s12069/label'])
  if self.Gyri.get('side')=='left':
    side = 'lh'
  elif self.Gyri.get('side')=='right':
    side = 'rh'
  else:
    context.write('Error in side')
    return
  
 
  context.write('mri_annotation2label --subject %s --hemi %s --annotation %s --labelbase %s'%(self.Gyri.get('subject'), side, self.Gyri.fullName()[self.Gyri.fullName().rfind('/')+4:], self.Gyri.fullPath()[self.Gyri.fullPath().rfind('/')+1:]))

  launchFreesurferCommand(context,
                          self.Gyri.get('_database'),
                          'mri_annotation2label',
                          '--subject', self.Gyri.get('subject'),
                          '--hemi', side,
                          '--annotation', self.Gyri.fullName()[self.Gyri.fullName().rfind('/')+4:],
                          '--labelbase', self.Gyri.fullPath()[self.Gyri.fullPath().rfind('/')+1:])


  context.write('mri_annotation2label --subject %s --hemi %s --annotation %s --labelbase %s'%(self.SulciGyri.get('subject'), side, self.SulciGyri.fullName()[self.SulciGyri.fullName().rfind('/')+4:], self.SulciGyri.fullPath()[self.SulciGyri.fullPath().rfind('/')+1:]))
  
  launchFreesurferCommand(context,
                          self.SulciGyri.get('_database'),
                          'mri_annotation2label',
                          '--subject', self.SulciGyri.get('subject'),
                          '--hemi', side,
                          '--annotation', self.SulciGyri.fullName()[self.SulciGyri.fullName().rfind('/')+4:],
                          '--labelbase', self.SulciGyri.fullPath()[self.SulciGyri.fullPath().rfind('/')+1:])


