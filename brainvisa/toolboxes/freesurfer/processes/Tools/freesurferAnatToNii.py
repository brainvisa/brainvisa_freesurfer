# -*- coding: utf-8 -*-
import os
from brainvisa.processes import *
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand

name = "03b Convert Freesurfer anatomical image to Nifti format"
userLevel = 2

signature = Signature(
  'AnatImage', ReadDiskItem('RawFreesurferAnat', 'FreesurferMGZ',
    enableConversion=False ),
  'NiiAnatImage', WriteDiskItem('RawFreesurferAnat', 'NIFTI-1 image'),
  )

def initialization(self):
  self.linkParameters('NiiAnatImage', 'AnatImage')
  
def execution(self, context):
  # mri_convert will not write a .minf, so we have to take care if it
  # already exists from a previous data
  if os.path.exists( self.NiiAnatImage.minfFileName() ):
    self.NiiAnatImage.clearMinf( saveMinf=True )
  launchFreesurferCommand( context, self.AnatImage.get('_database'),
                           'mri_convert',
                           self.AnatImage.fullPath(),
                           self.NiiAnatImage.fullPath() )
  self.NiiAnatImage.saveMinf()
  context.system('python', '-c', 'from freesurfer.setAnatTransformation import setAnatTransformation as f; f(\"%s\");'%(self.NiiAnatImage.fullPath()))
  self.NiiAnatImage.readAndUpdateMinf()

