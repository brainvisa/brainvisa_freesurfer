# -*- coding: utf-8 -*-
import os
from brainvisa.processes import *
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand
from brainvisa import registration

name = "Convert Freesurfer images to Nifti format"
userLevel = 2

signature = Signature(
  'AnatImage', ReadDiskItem('RawFreesurferAnat', 'FreesurferMGZ',
    enableConversion=False),
  'NiiAnatImage', WriteDiskItem('RawFreesurferAnat', 'NIFTI-1 image'),
  'NuImage', ReadDiskItem('Nu FreesurferAnat', 'FreesurferMGZ',
    enableConversion=False),
  'NiiNuImage', WriteDiskItem('Nu FreesurferAnat', 'NIFTI-1 image'),
  'RibbonImage', ReadDiskItem('Ribbon Freesurfer', 'FreesurferMGZ',
    enableConversion=False),
  'NiiRibbonImage', WriteDiskItem('Ribbon Freesurfer', 'NIFTI-1 image' ),
  'referential', ReadDiskItem( 'Referential of Raw T1 MRI', 'Referential' ),
)

def initialization(self):
  self.linkParameters( 'NiiAnatImage', 'AnatImage' )
  self.linkParameters( 'NuImage', 'AnatImage' )
  self.linkParameters( 'NiiNuImage', 'NuImage' )
  self.linkParameters( 'RibbonImage', 'AnatImage' )
  self.linkParameters( 'NiiRibbonImage', 'RibbonImage' )
  self.linkParameters( 'referential', 'AnatImage' )
  self.setOptional( 'referential' )

def execution(self, context):
  
  if os.path.exists( self.NiiAnatImage.minfFileName() ):
    context.write( 'removing residual .minf file %s' % self.NiiAnatImage.minfFileName() )
    os.unlink( self.NiiAnatImage.minfFileName() )
  if os.path.exists( self.NiiNuImage.minfFileName() ):
    context.write( 'removing residual .minf file %s' % self.NiiNuImage.minfFileName() )
    os.unlink( self.NiiNuImage.minfFileName() )
  if os.path.exists( self.NiiRibbonImage.minfFileName() ):
    context.write( 'removing residual .minf file %s' % self.NiiRibbonImage.minfFileName() )
    os.unlink( self.NiiRibbonImage.minfFileName() )
  
  # convert from .mgz to .nii with Freesurfer
  launchFreesurferCommand( context, '',
                           'mri_convert',
                           self.AnatImage.fullPath(),
                           self.NiiAnatImage.fullPath() )
  launchFreesurferCommand( context, '',
                           'mri_convert',
                           self.NuImage.fullPath(),
                           self.NiiNuImage.fullPath() )                        
  launchFreesurferCommand( context, '',
                           'mri_convert',
                           self.RibbonImage.fullPath(),
                           self.NiiRibbonImage.fullPath() )
                           
  # reset minf attributes in case there was an existing older diskitem
  self.NiiAnatImage._minfAttributes = {}
  self.NiiNuImage._minfAttributes = {}
  self.NiiRibbonImage._minfAttributes = {}
  self.NiiAnatImage.saveMinf()
  self.NiiNuImage.saveMinf()
  self.NiiRibbonImage.saveMinf()
  context.system('python', '-c', 'from freesurfer.setAnatTransformation import setAnatTransformation as f; f(\"%s\");'%(self.NiiAnatImage.fullPath()))
  context.system('python', '-c', 'from freesurfer.setAnatTransformation import setAnatTransformation as f; f(\"%s\");'%(self.NiiNuImage.fullPath()))
  context.system('python', '-c', 'from freesurfer.setAnatTransformation import setAnatTransformation as f; f(\"%s\");'%(self.NiiRibbonImage.fullPath()))
  self.NiiAnatImage.readAndUpdateMinf()
  self.NiiNuImage.readAndUpdateMinf()
  self.NiiRibbonImage.readAndUpdateMinf()
  
  # referential
  if self.referential is not None:
    self.NiiAnatImage.setMinf( 'referential', self.referential.uuid(),
      saveMinf=True )
    self.NiiNuImage.setMinf( 'referential', self.referential.uuid(),
      saveMinf=True ) 
    self.NiiRibbonImage.setMinf( 'referential', self.referential.uuid(),
      saveMinf=True )
  registration.getTransformationManager().copyReferential( self.referential,
    self.NiiAnatImage )
  registration.getTransformationManager().copyReferential( self.referential,
    self.NiiNuImage )  
  registration.getTransformationManager().copyReferential( self.referential,
    self.NiiRibbonImage ) 

