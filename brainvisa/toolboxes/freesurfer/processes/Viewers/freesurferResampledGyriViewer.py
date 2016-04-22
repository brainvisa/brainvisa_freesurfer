# -*- coding: utf-8 -*-
from brainvisa.processes import *
import shfjGlobals
from brainvisa import anatomist

name = 'Freesurfer resampled gyri viewer'
roles = ('viewer',)
userLevel = 0

def validation():
  anatomist.validation()

signature = Signature(
  'Gyri', ReadDiskItem('FreesurferResampledParcellationType',
    'anatomist Texture formats'),
  'WhiteMesh', ReadDiskItem('AimsWhite', 'anatomist mesh formats'),
)

def initialization( self ):
  self.linkParameters('WhiteMesh', 'Gyri')


def execution( self, context ):
  a=anatomist.Anatomist()
  return a.viewTextureOnMesh(self.WhiteMesh, self.Gyri, interpolation='rgb',
                             palette='freesurfer_gyri')
