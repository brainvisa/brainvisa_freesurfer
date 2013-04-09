# -*- coding: utf-8 -*-
from brainvisa.processes import *
from brainvisa import registration

name = 'Meshes inflate'
userlevel = 2

signature = Signature(
  'White', ReadDiskItem('AimsWhite', 'Aims mesh formats'),
  'InflatedWhite', WriteDiskItem('AimsInflatedWhite', 'Aims mesh formats'),
  'InflatedWhiteCurvTex', WriteDiskItem('AimsInflatedWhiteCurvTex', 'Aims Texture formats'),
  )

def initialization(self):
  self.linkParameters('InflatedWhite', 'White')
  self.linkParameters('InflatedWhiteCurvTex', 'White')

  
def execution(self, context):
  context.write(self.White.fullPath())
  context.system( 'AimsInflate', '-i', self.White.fullPath(), '-o',
                  self.InflatedWhite.fullPath(), '-c',
                  self.InflatedWhiteCurvTex.fullPath())
  tm = registration.getTransformationManager()
  tm.copyReferential( self.White, self.InflatedWhite )
