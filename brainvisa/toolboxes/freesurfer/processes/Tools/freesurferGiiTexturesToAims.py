import os
import sys
from brainvisa.processes import *

name = '13 Converting gifti textures to Aims texture format.'
userlevel = 2

signature = Signature(
    'GiftiCurv', ReadDiskItem('FreesurferCurvType', 'GIFTI File'),
  'GiftiAvgCurv', ReadDiskItem('FreesurferAvgCurvType', 'GIFTI File'),
  'GiftiCurvPial', ReadDiskItem('FreesurferCurvPialType', 'GIFTI File'),
  'GiftiThickness', ReadDiskItem('FreesurferThicknessType', 'GIFTI File'),

  'TexCurv', WriteDiskItem('FreesurferCurvType', 'Texture'),
  'TexAvgCurv', WriteDiskItem('FreesurferAvgCurvType', 'Texture'),
  'TexCurvPial', WriteDiskItem('FreesurferCurvPialType', 'Texture'),
  'TexThickness', WriteDiskItem('FreesurferThicknessType', 'Texture'),
)


def initialization(self):
    self.linkParameters('GiftiAvgCurv', 'GiftiCurv')
    self.linkParameters('GiftiCurvPial', 'GiftiCurv')
    self.linkParameters('GiftiThickness', 'GiftiCurv')
    self.linkParameters('TexCurv', 'GiftiCurv')
    self.linkParameters('TexAvgCurv', 'GiftiCurv')
    self.linkParameters('TexCurvPial', 'GiftiCurv')
    self.linkParameters('TexThickness', 'GiftiCurv')


def execution(self, context):
    context.write('Resample brain mesh.')

    context.write(self.GiftiAvgCurv.fullPath())
    context.system(os.path.basename(sys.executable), '-c', 'from freesurfer.giiToTex import giftiToTex as f; f(\"%s\", \"%s\");' %
                   (self.GiftiCurv.fullPath(), self.TexCurv.fullPath()))

    context.write(self.GiftiAvgCurv.fullPath())
    context.system(os.path.basename(sys.executable), '-c', 'from freesurfer.giiToTex import giftiToTex as f; f(\"%s\", \"%s\");' %
                   (self.GiftiAvgCurv.fullPath(), self.TexAvgCurv.fullPath()))

    context.write(self.GiftiCurvPial.fullPath())
    context.system(os.path.basename(sys.executable), '-c', 'from freesurfer.giiToTex import giftiToTex as f; f(\"%s\", \"%s\");' %
                   (self.GiftiCurvPial.fullPath(), self.TexCurvPial.fullPath()))

    context.write(self.GiftiThickness.fullPath())
    context.system(os.path.basename(sys.executable), '-c', 'from freesurfer.giiToTex import giftiToTex as f; f(\"%s\", \"%s\");' %
                   (self.GiftiThickness.fullPath(), self.TexThickness.fullPath()))
