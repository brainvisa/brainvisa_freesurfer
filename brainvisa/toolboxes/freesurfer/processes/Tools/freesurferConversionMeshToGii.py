# -*- coding: utf-8 -*-
from brainvisa.processes import *
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand

name = '04 Conversion of Freesurfer meshes to Gifti format'
userlevel = 2

signature = Signature(
  'Pial', ReadDiskItem('FreesurferType', 'FreesurferPial'),
  'White', ReadDiskItem('FreesurferType', 'FreesurferWhite'),
  'SphereReg', ReadDiskItem('FreesurferType', 'FreesurferSphereReg'),
  
  'PialGifti', WriteDiskItem('Pial', 'GIFTI File'),
  'WhiteGifti', WriteDiskItem('White', 'GIFTI File'),
  'SphereRegGifti', WriteDiskItem('SphereReg', 'GIFTI File'),
  'anat', ReadDiskItem( 'RawFreesurferAnat', 'FreesurferMGZ' ),
  )

def initialization(self):
  self.linkParameters('White', 'Pial')
  self.linkParameters('SphereReg', 'Pial')
  self.linkParameters('PialGifti', 'Pial')
  self.linkParameters('WhiteGifti', 'Pial')
  self.linkParameters('SphereRegGifti', 'Pial')
  self.setOptional( 'anat' )
  
def execution(self, context):
  context.write('Convert meshes in Freesurfer fromat to Gifti format.')
  context.write('mris_convert %s %s'%(self.Pial.fullPath(),self.PialGifti.fullPath()))
  database = ''
  launchFreesurferCommand( context, database, 'mris_convert', self.Pial.fullPath(), self.PialGifti.fullPath())
  context.write('mris_convert %s %s'%(self.White.fullPath(),self.WhiteGifti.fullPath()))
  launchFreesurferCommand( context, database,  'mris_convert', self.White.fullPath(), self.WhiteGifti.fullPath())
  context.write('mris_convert %s %s'%(self.SphereReg.fullPath(),self.SphereRegGifti.fullPath()))
  launchFreesurferCommand( context, database,  'mris_convert', self.SphereReg.fullPath(), self.SphereRegGifti.fullPath())

  if self.anat is not None:
    tm = registration.getTransformationManager()
    tm.copyReferential( self.anat, self.PialGifti )
    tm.copyReferential( self.anat, self.WhiteGifti )



