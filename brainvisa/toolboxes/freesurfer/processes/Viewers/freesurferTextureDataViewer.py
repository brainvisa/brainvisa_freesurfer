# -*- coding: utf-8 -*-
from brainvisa.processes import *
from brainvisa import anatomist

name = 'Freesurfer data textures viewer'
roles = ('viewer',)
userLevel = 0


def validation():
    anatomist.validation()

signature = Signature(
    'Texture', ReadDiskItem('DataTexture', 'anatomist Texture formats'),
  'WhiteMesh', ReadDiskItem('White', 'anatomist mesh formats'),
)


def initialization(self):
    self.linkParameters('WhiteMesh', 'Texture')


def execution(self, context):
    a = anatomist.Anatomist()
    return a.viewTextureOnMesh(self.WhiteMesh, self.Texture)
