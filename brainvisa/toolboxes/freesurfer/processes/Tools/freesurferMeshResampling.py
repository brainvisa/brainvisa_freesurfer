# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import sys
from brainvisa.processes import *
from brainvisa import registration

name = 'Mesh resampling'
userlevel = 2

signature = Signature(
    'PialMesh', ReadDiskItem('Pial', 'Aims mesh formats', enableConversion=0),
  'WhiteMesh', ReadDiskItem('White', 'Aims mesh formats'),
  'destination', ReadDiskItem('Ico Mesh', 'Aims mesh formats'),
  'Isin', ReadDiskItem('BaseFreesurferType', 'FreesurferIsin'),
  'ResampledPialMesh', WriteDiskItem('ResampledPial', 'Aims mesh formats'),
  'ResampledWhiteMesh', WriteDiskItem('ResampledWhite', 'Aims mesh formats'),
)


def initialization(self):
    self.linkParameters('WhiteMesh', 'PialMesh')
    self.linkParameters('Isin', 'PialMesh')
    self.linkParameters('destination', 'PialMesh')
    self.linkParameters('ResampledPialMesh', 'PialMesh')
    self.linkParameters('ResampledWhiteMesh', 'PialMesh')


def execution(self, context):
    context.write('Resample brain mesh.')

    context.write('%s -c \"from freesurfer.regularizeMeshFromIsin import regularizeMesh as f; f(\"%s\", \"%s\", \"%s\", \"%s\");\#' %
                  (os.path.basename(sys.executable), self.PialMesh.fullPath(), self.Isin.fullPath(), self.ResampledPialMesh.fullPath(), self.destination.fullPath()))
    context.system(os.path.basename(sys.executable), '-c', 'from freesurfer.regularizeMeshFromIsin import regularizeMeshAims as f; f(\"%s\", \"%s\", \"%s\", \"%s\")' %
                   (self.PialMesh.fullPath(), self.Isin.fullPath(), self.ResampledPialMesh.fullPath(), self.destination.fullPath()))

    context.write('%s -c \"from freesurfer.regularizeMeshFromIsin import regularizeMesh as f; f(\"%s\", \"%s\", \"%s\", \"%s\");\#' %
                  (os.path.basename(sys.executable), self.WhiteMesh.fullPath(), self.Isin.fullPath(), self.ResampledWhiteMesh.fullPath(), self.destination.fullPath()))
    context.system(os.path.basename(sys.executable), '-c', 'from freesurfer.regularizeMeshFromIsin import regularizeMeshAims as f; f(\"%s\", \"%s\", \"%s\", \"%s\")' %
                   (self.WhiteMesh.fullPath(), self.Isin.fullPath(), self.ResampledWhiteMesh.fullPath(), self.destination.fullPath()))

    self.ResampledPialMesh.setMinf('material',
                                   {'front_face': 'counterclockwise'}, saveMinf=True)
    self.ResampledWhiteMesh.setMinf('material',
                                    {'front_face': 'counterclockwise'}, saveMinf=True)
    tm = registration.getTransformationManager()
    tm.copyReferential(self.PialMesh, self.ResampledPialMesh)
    tm.copyReferential(self.WhiteMesh, self.ResampledWhiteMesh)
