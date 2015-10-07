# -*- coding: utf-8 -*-
import os
from brainvisa.processes import *
from brainvisa import registration

name = 'Conversion of meshes to aims referential'
userlevel = 2

signature = Signature(
    'ResampledPialMesh', ReadDiskItem('ResampledPial', 'Aims mesh formats'),
    'ResampledWhiteMesh', ReadDiskItem('ResampledWhite', 'Aims mesh formats'),
    'bv_anat', ReadDiskItem('RawFreesurferAnat', 'Aims readable volume formats'),
    'AimsPial', WriteDiskItem('AimsPial', 'Aims mesh formats'),
    'AimsWhite', WriteDiskItem('AimsWhite', 'Aims mesh formats',
                               exactType=True),
)

def initialization( self ):
  self.linkParameters( 'ResampledWhiteMesh', 'ResampledPialMesh' )
  self.linkParameters( 'bv_anat', 'ResampledPialMesh' )
  self.linkParameters( 'AimsPial', 'ResampledPialMesh' )
  self.linkParameters( 'AimsWhite', 'ResampledPialMesh' )

def execution(self, context):
  context.write('Conversion to Aims ref.')

  cmd = 'from freesurfer.freesurferMeshToAimsMesh import freesurferMeshToAimsMesh as f;'

  context.write('python -c '+cmd+' f(\"%s\", \"%s\", \"%s\");'%(self.ResampledPialMesh.fullPath(), self.bv_anat.fullPath(), self.AimsPial.fullPath()))
  context.system('python', '-c', cmd+'f(\"%s\", \"%s\", \"%s\");'%(self.ResampledPialMesh.fullPath(), self.bv_anat.fullPath(), self.AimsPial.fullPath()))

  context.write('python -c '+cmd+' f(\"%s\", \"%s\", \"%s\");'%(self.ResampledWhiteMesh.fullPath(), self.bv_anat.fullPath(), self.AimsWhite.fullPath()))
  context.system('python', '-c', cmd+'f(\"%s\", \"%s\", \"%s\");'%(self.ResampledWhiteMesh.fullPath(), self.bv_anat.fullPath(), self.AimsWhite.fullPath()))

  context.write( 'material:', self.AimsPial.get( 'material' ) )
  if self.AimsPial.get( 'material' ):
    self.AimsPial.removeMinf( 'material', saveMinf=True )
  if self.AimsWhite.get( 'material' ):
    self.AimsWhite.removeMinf( 'material', saveMinf=True )
  tm = registration.getTransformationManager()
  tm.copyReferential( self.bv_anat, self.AimsPial )
  tm.copyReferential( self.bv_anat, self.AimsWhite )
