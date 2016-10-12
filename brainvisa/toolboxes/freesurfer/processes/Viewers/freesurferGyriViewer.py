# -*- coding: utf-8 -*-
from brainvisa.processes import *
from brainvisa import anatomist

name = 'Freesurfer gyri viewer'
roles = ('viewer',)
userLevel = 0

def validation():
  anatomist.validation()

signature = Signature(
  'Gyri', ReadDiskItem('FreesurferParcellationType',
    'Anatomist Texture formats'),
  'WhiteMesh', ReadDiskItem('White', 'Anatomist mesh formats' ),
)

def initialization( self ):
  self.linkParameters('WhiteMesh', 'Gyri')


def execution( self, context ):
  a=anatomist.Anatomist()
  return a.viewTextureOnMesh(self.WhiteMesh, self.Gyri, interpolation='rgb')
