from neuroProcesses import *
import shfjGlobals
from brainvisa import anatomist

name = 'Freesurfer mesh viewer'
roles = ('viewer',)
userLevel = 0

def validation():
  anatomist.validation()

signature = Signature(
  'freesurferMesh', ReadDiskItem('FreesurferMesh', 'MESH mesh', enableConversion=0),
)

def initialization( self ):
  pass


def execution( self, context ):
  a=anatomist.Anatomist()
  return a.viewMesh(self.freesurferMesh)
