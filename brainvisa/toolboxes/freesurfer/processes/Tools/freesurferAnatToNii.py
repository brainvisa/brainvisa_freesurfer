# -*- coding: utf-8 -*-
import os
from brainvisa.processes import *
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand
from brainvisa import registration

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
  launchFreesurferCommand( context, '',
                           'mri_convert',
                           self.AnatImage.fullPath(),
                           self.NiiAnatImage.fullPath() )
  self.NiiAnatImage.saveMinf()
  context.system('python', '-c', 'from freesurfer.setAnatTransformation import setAnatTransformation as f; f(\"%s\");'%(self.NiiAnatImage.fullPath()))
  self.NiiAnatImage.readAndUpdateMinf()
  registration.getTransformationManager().copyReferential( self.AnatImage,
    self.NiiAnatImage )

