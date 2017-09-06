# -*- coding: utf-8 -*-
import os, sys
from brainvisa.processes import *
from brainvisa import registration

name = 'Conversion of native (unresampled) meshes to aims referential'
userlevel = 2

signature = Signature(
    'PialMesh', ReadDiskItem('Pial', 'Aims mesh formats'),
    'WhiteMesh', ReadDiskItem('White', 'Aims mesh formats'),
    'bv_anat', ReadDiskItem('FreesurferAnat', 'Aims readable volume formats'),
    'AimsNativePial', WriteDiskItem('AimsNativePial', 'Aims mesh formats'),
    'AimsNativeWhite', WriteDiskItem('AimsNativeWhite', 'Aims mesh formats'),
)

def initialization( self ):
  self.linkParameters( 'WhiteMesh', 'PialMesh' )
  self.linkParameters( 'bv_anat', 'PialMesh' )
  self.linkParameters( 'AimsNativePial', 'PialMesh' )
  self.linkParameters( 'AimsNativeWhite', 'PialMesh' )

def execution(self, context):
  context.write('Conversion to Aims ref.')

  cmd = 'from freesurfer.freesurferMeshToAimsMesh import freesurferMeshToAimsMesh as f;'

  context.write('%s -c '+cmd+' f(\"%s\", \"%s\", \"%s\");'%(os.path.basename(sys.executable), self.PialMesh.fullPath(), self.bv_anat.fullPath(), self.AimsNativePial.fullPath()))
  context.system(os.path.basename(sys.executable), '-c', cmd+'f(\"%s\", \"%s\", \"%s\");'%(self.PialMesh.fullPath(), self.bv_anat.fullPath(), self.AimsNativePial.fullPath()))

  context.write('%s -c '+cmd+' f(\"%s\", \"%s\", \"%s\");'%(os.path.basename(sys.executable), self.WhiteMesh.fullPath(), self.bv_anat.fullPath(), self.AimsNativeWhite.fullPath()))
  context.system(os.path.basename(sys.executable), '-c', cmd+'f(\"%s\", \"%s\", \"%s\");'%(self.WhiteMesh.fullPath(), self.bv_anat.fullPath(), self.AimsNativeWhite.fullPath()))

  context.write( 'material:', self.AimsNativePial.get( 'material' ) )
  if self.AimsNativePial.get( 'material' ):
    self.AimsNativePial.removeMinf( 'material', saveMinf=True )
  if self.AimsNativeWhite.get( 'material' ):
    self.AimsNativeWhite.removeMinf( 'material', saveMinf=True )
  tm = registration.getTransformationManager()
  tm.copyReferential( self.bv_anat, self.AimsNativePial )
  tm.copyReferential( self.bv_anat, self.AimsNativeWhite )
