import os
from brainvisa.processes import *
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand

name = "03b Convert Freesurfer anatomical image to Nifti format"
userLevel = 2

signature = Signature(
  'AnatImage', ReadDiskItem('FreesurferAnat', 'FreesurferMGZ'),
  'NiiAnatImage', WriteDiskItem('FreesurferAnat', 'NIFTI-1 image'),
  )

def initialization(self):
  self.linkParameters('NiiAnatImage', 'AnatImage')
  
def execution(self, context):
  launchFreesurferCommand( context, self.AnatImage.get('_database'),
                           'mri_convert',
                           self.AnatImage.fullPath(),
                           self.NiiAnatImage.fullPath() )
  
  context.system('python', '-c', 'from freesurfer.setAnatTransformation import setAnatTransformation as f; f(\"%s\");'%(self.NiiAnatImage.fullPath()))

