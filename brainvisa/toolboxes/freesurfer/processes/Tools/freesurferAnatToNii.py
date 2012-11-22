# -*- coding: utf-8 -*-
import os
from brainvisa.processes import *
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand

name = "03b Convert Freesurfer anatomical image to Nifti format"
userLevel = 2

signature = Signature(
  'AnatImage', ReadDiskItem('RawFreesurferAnat', 'FreesurferMGZ'),
  'NiiAnatImage', WriteDiskItem('RawFreesurferAnat', 'NIFTI-1 image'),
  'database', ReadDiskItem( 'Directory', 'Directory' ),
  )

def initialization(self):
  def linkDB( self, dummy ):
    if self.AnatImage:
      return self.AnatImage.get('_database')
  self.linkParameters('NiiAnatImage', 'AnatImage')
  self.linkParameters('database', 'AnatImage', linkDB)
  
def execution(self, context):
  launchFreesurferCommand( context, self.database.fullPath(),
                           'mri_convert',
                           self.AnatImage.fullPath(),
                           self.NiiAnatImage.fullPath() )
  
  context.system('python', '-c', 'from freesurfer.setAnatTransformation import setAnatTransformation as f; f(\"%s\");'%(self.NiiAnatImage.fullPath()))

