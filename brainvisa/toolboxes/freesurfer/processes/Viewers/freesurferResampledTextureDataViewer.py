# -*- coding: utf-8 -*-
from brainvisa.processes import *
import shfjGlobals
from brainvisa import anatomist

name = 'Freesurfer resampled data textures viewer'
roles = ('viewer',)
userLevel = 0

def validation():
  anatomist.validation()

signature = Signature(
  'Texture', ReadDiskItem('ResampledDataTexture', 'anatomist Texture formats'),
  'WhiteMesh', ReadDiskItem('AimsWhite', 'anatomist mesh formats'),
)

def initialization( self ):
  self.linkParameters('WhiteMesh', 'Texture')


def execution( self, context ):
  a=anatomist.Anatomist()
  return a.viewTextureOnMesh(self.WhiteMesh, self.Texture)
