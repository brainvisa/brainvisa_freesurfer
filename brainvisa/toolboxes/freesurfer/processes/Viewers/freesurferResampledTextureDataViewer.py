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
    'Texture', ReadDiskItem('ResampledDataTexture',
                            'anatomist Texture formats'),
    'WhiteMesh', ReadDiskItem('AimsWhite', 'anatomist mesh formats'),
    "prefer_inflated_meshes", Boolean(),
)

def initialization( self ):
    def link_mesh(self, dummy):
        if self.Texture is not None:
            if self.prefer_inflated_meshes:
                infl1 = 'Yes'
                infl2 = 'No'
            else:
                infl1 = 'No'
                infl2 = 'Yes'
            mesh_type = self.signature["WhiteMesh"]
            res = mesh_type.findValue(self.Texture,
                                      requiredAttributes={"inflated": infl1})
            if res is None:
                res = mesh_type.findValue(
                    self.Texture, requiredAttributes={"inflated": infl2})
            if res is None:
                res = self.Texture
            return res

    self.linkParameters('WhiteMesh', ['Texture', 'prefer_inflated_meshes'],
                        link_mesh)


def execution( self, context ):
    a=anatomist.Anatomist()
    return a.viewTextureOnMesh(self.WhiteMesh, self.Texture)
