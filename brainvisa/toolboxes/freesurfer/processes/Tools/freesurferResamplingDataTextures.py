from brainvisa.processes import *

name = '14 Resampling freesurfer data textures.'
userlevel = 2

signature = Signature(
  'OriginalMesh', ReadDiskItem('White', 'MESH mesh', enableConversion=0),
  'Isin', ReadDiskItem('BaseFreesurferType', 'FreesurferIsin'),
  #
  'Curv', ReadDiskItem('FreesurferCurvType', 'Texture'),
  'AvgCurv', ReadDiskItem('FreesurferAvgCurvType', 'Texture'),
  'CurvPial', ReadDiskItem('FreesurferCurvPialType', 'Texture'),
  'Thickness', ReadDiskItem('FreesurferThicknessType', 'Texture'),
  #
  'ResampledCurv', WriteDiskItem('ResampledFreesurferCurvType', 'Texture'),
  'ResampledAvgCurv', WriteDiskItem('ResampledFreesurferAvgCurvType', 'Texture'),
  'ResampledCurvPial', WriteDiskItem('ResampledFreesurferCurvPialType', 'Texture'),
  'ResampledThickness', WriteDiskItem('ResampledFreesurferThicknessType', 'Texture'),
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
  context.system('python', '-c', 'from freesurfer.regularizeTexture import regularizeTexture as f; f(\"%s\", \"%s\", \"%s\", \"%s\");'%(
    self.Isin.fullPath(), self.OriginalMesh.fullPath(),
    self.Curv.fullPath(), self.ResampledCurv.fullPath()))

  context.write(self.AvgCurv.fullPath())
  context.system('python', '-c', 'from freesurfer.regularizeTexture import regularizeTexture as f; f(\"%s\", \"%s\", \"%s\", \"%s\");'%(
    self.Isin.fullPath(), self.OriginalMesh.fullPath(),
    self.AvgCurv.fullPath(), self.ResampledAvgCurv.fullPath()))

  context.write(self.CurvPial.fullPath())
  context.system('python', '-c', 'from freesurfer.regularizeTexture import regularizeTexture as f; f(\"%s\", \"%s\", \"%s\", \"%s\");'%(
    self.Isin.fullPath(), self.OriginalMesh.fullPath(),
    self.CurvPial.fullPath(), self.ResampledCurvPial.fullPath()))

  context.write(self.Thickness.fullPath())
  context.system('python', '-c', 'from freesurfer.regularizeTexture import regularizeTexture as f; f(\"%s\", \"%s\", \"%s\", \"%s\");'%(
    self.Isin.fullPath(), self.OriginalMesh.fullPath(),
    self.Thickness.fullPath(), self.ResampledThickness.fullPath()))
