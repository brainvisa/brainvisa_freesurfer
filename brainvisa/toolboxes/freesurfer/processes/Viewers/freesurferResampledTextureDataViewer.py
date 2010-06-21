from neuroProcesses import *
import shfjGlobals
from brainvisa import anatomist

name = 'Freesurfer resampled data textures viewer'
roles = ('viewer',)
userLevel = 0

def validation():
  anatomist.validation()

signature = Signature(
  'Texture', ReadDiskItem('ResampledDataTexture', 'Texture'),
  'WhiteMesh', ReadDiskItem('AimsWhite', 'MESH mesh', enableConversion=0),
)

def initialization( self ):
  self.linkParameters('WhiteMesh', 'Texture')


def execution( self, context ):
  a=anatomist.Anatomist()
  return a.viewTextureOnMesh(self.WhiteMesh, self.Texture)
