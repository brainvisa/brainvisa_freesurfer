# -*- coding: utf-8 -*-
from __future__ import absolute_import
from brainvisa.processes import *
from brainvisa import anatomist

name = 'Freesurfer mesh viewer'
roles = ('viewer',)
userLevel = 0


def validation():
    anatomist.validation()

signature = Signature(
    'freesurferMesh', ReadDiskItem('FreesurferMesh', 'anatomist mesh formats'),
)


def initialization(self):
    pass


def execution(self, context):
    a = anatomist.Anatomist()
    return a.viewMesh(self.freesurferMesh)
