# -*- coding: utf-8 -*-
from brainvisa.processes import *
from freesurfer.brainvisaFreesurfer \
    import launchFreesurferCommand, testFreesurferCommand
from brainvisa import registration

name = 'Conversion of Freesurfer meshes to Gifti format'
userlevel = 2


def validation():
    testFreesurferCommand()

signature = Signature(
  'Pial', ReadDiskItem('FreesurferType', 'FreesurferPial'),
  'White', ReadDiskItem('FreesurferType', 'FreesurferWhite'),
  'SphereReg', ReadDiskItem('FreesurferType', 'FreesurferSphereReg'),
  
  'PialGifti', WriteDiskItem('Pial', 'GIFTI File'),
  'WhiteGifti', WriteDiskItem('White', 'GIFTI File'),
  'SphereRegGifti', WriteDiskItem('SphereReg', 'GIFTI File'),
  'meshes_referential', ReadDiskItem( 'Referential of Pial', 'Referential' ),
)

def initialization(self):
  self.linkParameters('White', 'Pial')
  self.linkParameters('SphereReg', 'Pial')
  self.linkParameters('PialGifti', 'Pial')
  self.linkParameters('WhiteGifti', 'Pial')
  self.linkParameters('SphereRegGifti', 'Pial')
  self.linkParameters('meshes_referential', 'PialGifti')
  self.setOptional( 'meshes_referential', 'SphereReg', 'SphereRegGifti' )

def execution(self, context):
  if self.SphereRegGifti is not None and self.SphereReg is None:
    context.warning( 'SphereReg parameter is not set: SphereRegGifti will not be written.' )
  context.write('Convert meshes in Freesurfer fromat to Gifti format.')
  context.write('mris_convert %s %s'%(self.Pial.fullPath(),self.PialGifti.fullPath()))
  database = ''
  launchFreesurferCommand( context, database, 'mris_convert', self.Pial.fullPath(), self.PialGifti.fullPath())
  context.write('mris_convert %s %s'%(self.White.fullPath(),self.WhiteGifti.fullPath()))
  launchFreesurferCommand( context, database,  'mris_convert', self.White.fullPath(), self.WhiteGifti.fullPath())
  self.PialGifti.setMinf( 'material',
    { 'front_face': 'counterclockwise' }, saveMinf=True )
  if self.SphereReg is not None and self.SphereRegGifti is not None:
    context.write('mris_convert %s %s'%(self.SphereReg.fullPath(),self.SphereRegGifti.fullPath()))
    launchFreesurferCommand( context, database,  'mris_convert', self.SphereReg.fullPath(), self.SphereRegGifti.fullPath())
    self.WhiteGifti.setMinf( 'material',
      { 'front_face': 'counterclockwise' }, saveMinf=True )

  if self.meshes_referential is not None:
    tm = registration.getTransformationManager()
    tm.copyReferential( self.meshes_referential, self.PialGifti )
    tm.copyReferential( self.meshes_referential, self.WhiteGifti )



