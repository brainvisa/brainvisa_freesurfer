from brainvisa.processes import *
import shfjGlobals
from brainvisa import anatomist

name = 'Freesurfer resampled gyri viewer for both hemispheres'
roles = ('viewer',)
userLevel = 0

def validation():
  anatomist.validation()

signature = Signature(
  'Gyri', ReadDiskItem('FreesurferResampledBothParcellationType', 'Texture'),
  'BrainMesh', ReadDiskItem('AimsBothWhite', 'MESH mesh', enableConversion=0),
)

def initialization( self ):
  self.linkParameters('BrainMesh', 'Gyri')


def execution( self, context ):
  a=anatomist.Anatomist()
  return a.viewTextureOnMesh(self.BrainMesh, self.Gyri)
