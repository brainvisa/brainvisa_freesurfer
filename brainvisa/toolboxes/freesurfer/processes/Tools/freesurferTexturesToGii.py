# -*- coding: utf-8 -*-
from __future__ import absolute_import
from brainvisa.processes import *
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand

name = 'Converting freesurfer textures to Gifti format.'
userlevel = 2

signature = Signature(
    'Curv', ReadDiskItem('BaseFreesurferType', 'FreesurferCurv'),
  'AvgCurv', ReadDiskItem('BaseFreesurferType', 'FreesurferAvgCurv'),
  'CurvPial', ReadDiskItem('BaseFreesurferType', 'FreesurferCurvPial'),
  'Thickness', ReadDiskItem('BaseFreesurferType', 'FreesurferThickness'),

  'GiftiCurv', WriteDiskItem('FreesurferCurvType', 'GIFTI File'),
  'GiftiAvgCurv', WriteDiskItem('FreesurferAvgCurvType', 'GIFTI File'),
  'GiftiCurvPial', WriteDiskItem('FreesurferCurvPialType', 'GIFTI File'),
  'GiftiThickness', WriteDiskItem('FreesurferThicknessType', 'GIFTI File'),

)


def initialization(self):
    self.linkParameters('AvgCurv', 'Curv')
    self.linkParameters('CurvPial', 'Curv')
    self.linkParameters('Thickness', 'Curv')
    self.linkParameters('GiftiCurv', 'Curv')
    self.linkParameters('GiftiAvgCurv', 'Curv')
    self.linkParameters('GiftiCurvPial', 'Curv')
    self.linkParameters('GiftiThickness', 'Curv')


def execution(self, context):
    context.write('Resample brain mesh.')
    database = ''
    launchFreesurferCommand(context, database,
                            'mri_convert', self.Curv.fullPath(),
                            self.GiftiCurv.fullPath())
    launchFreesurferCommand(context, database,
                            'mri_convert', self.AvgCurv.fullPath(),
                            self.GiftiAvgCurv.fullPath())
    launchFreesurferCommand(context, database,
                            'mri_convert', self.CurvPial.fullPath(),
                            self.GiftiCurvPial.fullPath())
    launchFreesurferCommand(context, database,
                            'mri_convert', self.Thickness.fullPath(),
                            self.GiftiThickness.fullPath())
