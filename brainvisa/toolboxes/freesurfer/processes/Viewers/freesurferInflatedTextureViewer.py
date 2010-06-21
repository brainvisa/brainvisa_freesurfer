from neuroProcesses import *
import shfjGlobals
from brainvisa import anatomist

name = 'Freesurfer inflated data viewer'
roles = ('viewer',)
userLevel = 0

def validation():
  anatomist.validation()

signature = Signature(
  'Texture', ReadDiskItem('AimsInflated', 'Texture'),
  'WhiteMesh', ReadDiskItem('AimsInflatedWhite', 'MESH mesh', enableConversion=0),
)

def initialization( self ):
  self.linkParameters('WhiteMesh', 'Texture')


def execution( self, context ):
  a=anatomist.Anatomist()
  return a.viewTextureOnMesh(self.WhiteMesh, self.Texture)
