from neuroProcesses import *
import shfjGlobals
from brainvisa import anatomist

name = 'Freesurfer resampled gyri viewer'
roles = ('viewer',)
userLevel = 0

def validation():
  anatomist.validation()

signature = Signature(
  'Gyri', ReadDiskItem('FreesurferResampledParcellationType', 'Texture'),
  'WhiteMesh', ReadDiskItem('AimsWhite', 'MESH mesh', enableConversion=0),
)

def initialization( self ):
  self.linkParameters('WhiteMesh', 'Gyri')


def execution( self, context ):
  a=anatomist.Anatomist()
  return a.viewTextureOnMesh(self.WhiteMesh, self.Gyri)
