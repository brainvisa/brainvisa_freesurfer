import os
from neuroProcesses import *

name = '18 Meshes normalization'
userlevel = 2

signature = Signature(
    'whiteMesh', ReadDiskItem('AimsWhite', 'MESH mesh'),
    'anat', ReadDiskItem('Raw T1 MRI', 'NIFTI-1 image'),
    'matrix', ReadDiskItem('SPM Transformation Parameters', 'Matlab file'),
    'normAnat', ReadDiskItem('Raw T1 MRI', 'NIFTI-1 image',
                             requiredAttributes = {'normalized' : 'yes'}),
    'whiteNormMesh', WriteDiskItem('AimsNormalizedWhite', 'MESH mesh'),
)

def initialization( self ):
  self.linkParameters( 'matrix', 'whiteMesh' )
  self.linkParameters( 'anat', 'whiteMesh' )
  self.linkParameters( 'normAnat', 'whiteMesh' )
  self.linkParameters( 'whiteNormMesh', 'whiteMesh' )


def execution(self, context):
  context.write(self.whiteMesh.fullPath())

  context.system('python', '-c', 'from freesurfer.normalizeMesh import normalizeMesh as f; f(\"%s\", \"%s\", \"%s\", \"%s\", \"%s\");'%(self.anat.fullPath(), self.matrix.fullPath(), self.normAnat.fullPath(), self.whiteMesh.fullPath(), self.whiteNormMesh.fullPath()))

