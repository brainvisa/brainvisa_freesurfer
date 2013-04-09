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
  'referential', ReadDiskItem( 'Referential of Raw T1 MRI', 'Referential' ),
)

def initialization(self):
  self.linkParameters( 'NiiAnatImage', 'AnatImage' )
  self.linkParameters( 'referential', 'AnatImage' )
  self.setOptional( 'referential' )

def execution(self, context):
  if os.path.exists( self.NiiAnatImage.minfFileName() ):
    context.write( 'removing residual .minf file %s' % self.NiiAnatImage.minfFileName() )
    os.unlink( self.NiiAnatImage.minfFileName() )
  launchFreesurferCommand( context, '',
                           'mri_convert',
                           self.AnatImage.fullPath(),
                           self.NiiAnatImage.fullPath() )
  # reset minf attributes in case there was an existing older diskitem
  self.NiiAnatImage._minfAttributes = {}
  self.NiiAnatImage.saveMinf()
  context.system('python', '-c', 'from freesurfer.setAnatTransformation import setAnatTransformation as f; f(\"%s\");'%(self.NiiAnatImage.fullPath()))
  self.NiiAnatImage.readAndUpdateMinf()
  if self.referential is not None:
    self.NiiAnatImage.setMinf( 'referential', self.referential.uuid(),
      saveMinf=True )
  registration.getTransformationManager().copyReferential( self.referential,
    self.NiiAnatImage )

