# -*- coding: utf-8 -*-
from brainvisa.processes import *
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand

name = 'Resample label textures.'
userlevel = 2

signature = Signature(
  'WhiteMesh', ReadDiskItem('White', 'Aims mesh formats', enableConversion=0),
  'Isin', ReadDiskItem('BaseFreesurferType', 'FreesurferIsin'),
  'Gyri', ReadDiskItem('FreesurferGyri', 'Aims Texture formats'),
  'SulciGyri', ReadDiskItem('FreesurferSulciGyri', 'Aims Texture formats'),
  'ResampledGyri', WriteDiskItem('ResampledGyri', 'Aims Texture formats'),
  'ResampledSulciGyri', WriteDiskItem('ResampledSulciGyri', 'Aims Texture formats'),
  )

def initialization(self):
  self.linkParameters('Isin', 'WhiteMesh')
  self.linkParameters('Gyri', 'WhiteMesh')
  self.linkParameters('SulciGyri', 'WhiteMesh')
  self.linkParameters('ResampledGyri', 'WhiteMesh')
  self.linkParameters('ResampledSulciGyri', 'WhiteMesh')

  
def execution(self, context):
  context.write('Resample  brain mesh.')

  context.system('python2', '-c', 'from freesurfer.regularizeParcelTexture import regularizeParcelTexture as f; f(\"%s\", \"%s\", \"%s\", \"%s\");'%(self.Isin.fullPath(), self.WhiteMesh.fullPath(), self.Gyri.fullPath(), self.ResampledGyri.fullPath()))

  context.system('python2', '-c', 'from freesurfer.regularizeParcelTexture import regularizeParcelTexture as f; f(\"%s\", \"%s\", \"%s\", \"%s\");'%(self.Isin.fullPath(), self.WhiteMesh.fullPath(), self.SulciGyri.fullPath(), self.ResampledSulciGyri.fullPath()))

