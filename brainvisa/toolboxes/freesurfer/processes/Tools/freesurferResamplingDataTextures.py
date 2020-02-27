# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import sys
from brainvisa.processes import *

name = 'Resampling freesurfer data textures.'
userlevel = 2

signature = Signature(
    'OriginalMesh', ReadDiskItem(
        'White', 'Aims mesh formats', enableConversion=0),
  'Isin', ReadDiskItem('BaseFreesurferType', 'FreesurferIsin'),
  #
  'Curv', ReadDiskItem('FreesurferCurvType', 'Aims Texture formats'),
  'AvgCurv', ReadDiskItem('FreesurferAvgCurvType', 'Aims Texture formats'),
  'CurvPial', ReadDiskItem('FreesurferCurvPialType', 'Aims Texture formats'),
  'Thickness', ReadDiskItem('FreesurferThicknessType', 'Aims Texture formats'),
  #
  'ResampledCurv', WriteDiskItem(
      'ResampledFreesurferCurvType', 'Aims Texture formats'),
  'ResampledAvgCurv', WriteDiskItem(
      'ResampledFreesurferAvgCurvType', 'Aims Texture formats'),
  'ResampledCurvPial', WriteDiskItem(
      'ResampledFreesurferCurvPialType', 'Aims Texture formats'),
  'ResampledThickness', WriteDiskItem(
      'ResampledFreesurferThicknessType', 'Aims Texture formats'),
)


def initialization(self):
    self.linkParameters('Isin', 'OriginalMesh')
    self.linkParameters('Curv', 'OriginalMesh')
    self.linkParameters('AvgCurv', 'OriginalMesh')
    self.linkParameters('CurvPial', 'OriginalMesh')
    self.linkParameters('Thickness', 'OriginalMesh')
    self.linkParameters('ResampledCurv', 'OriginalMesh')
    self.linkParameters('ResampledAvgCurv', 'OriginalMesh')
    self.linkParameters('ResampledCurvPial', 'OriginalMesh')
    self.linkParameters('ResampledThickness', 'OriginalMesh')


def execution(self, context):
    context.write('Resample brain mesh.')

    context.write(self.Curv.fullPath())
    context.system(os.path.basename(sys.executable), '-c', 'from freesurfer.regularizeTexture import regularizeTexture as f; f(\"%s\", \"%s\", \"%s\", \"%s\");' % (
                   self.Isin.fullPath(), self.OriginalMesh.fullPath(),
                   self.Curv.fullPath(), self.ResampledCurv.fullPath()))

    context.write(self.AvgCurv.fullPath())
    context.system(os.path.basename(sys.executable), '-c', 'from freesurfer.regularizeTexture import regularizeTexture as f; f(\"%s\", \"%s\", \"%s\", \"%s\");' % (
                   self.Isin.fullPath(), self.OriginalMesh.fullPath(),
                   self.AvgCurv.fullPath(), self.ResampledAvgCurv.fullPath()))

    context.write(self.CurvPial.fullPath())
    context.system(os.path.basename(sys.executable), '-c', 'from freesurfer.regularizeTexture import regularizeTexture as f; f(\"%s\", \"%s\", \"%s\", \"%s\");' % (
                   self.Isin.fullPath(), self.OriginalMesh.fullPath(),
                   self.CurvPial.fullPath(), self.ResampledCurvPial.fullPath()))

    context.write(self.Thickness.fullPath())
    context.system(os.path.basename(sys.executable), '-c', 'from freesurfer.regularizeTexture import regularizeTexture as f; f(\"%s\", \"%s\", \"%s\", \"%s\");' % (
                   self.Isin.fullPath(), self.OriginalMesh.fullPath(),
                   self.Thickness.fullPath(), self.ResampledThickness.fullPath()))
