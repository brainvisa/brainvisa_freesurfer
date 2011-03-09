# -*- coding: utf-8 -*-
from neuroProcesses import *

name = '07 Mesh resampling'
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
  
  context.write('python -c \"from freesurfer.regularizeMeshFromIsin import regularizeMesh as f; f(\"%s\", \"%s\", \"%s\", \"%s\");\#'%(self.PialMesh.fullPath(), self.Isin.fullPath(), self.ResampledPialMesh.fullPath(), self.destination.fullPath()))
  context.system('python', '-c', 'from freesurfer.regularizeMeshFromIsin import regularizeMesh as f; f(\"%s\", \"%s\", \"%s\", \"%s\")'%(self.PialMesh.fullPath(), self.Isin.fullPath(), self.ResampledPialMesh.fullPath(), self.destination.fullPath()))

  context.write('python -c \"from freesurfer.regularizeMeshFromIsin import regularizeMesh as f; f(\"%s\", \"%s\", \"%s\", \"%s\");\#'%(self.WhiteMesh.fullPath(), self.Isin.fullPath(), self.ResampledWhiteMesh.fullPath(), self.destination.fullPath()))
  context.system('python', '-c', 'from freesurfer.regularizeMeshFromIsin import regularizeMesh as f; f(\"%s\", \"%s\", \"%s\", \"%s\")'%(self.WhiteMesh.fullPath(), self.Isin.fullPath(), self.ResampledWhiteMesh.fullPath(), self.destination.fullPath()))

  
