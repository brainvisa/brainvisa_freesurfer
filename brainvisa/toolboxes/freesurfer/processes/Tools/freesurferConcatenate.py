# -*- coding: utf-8 -*-
from brainvisa.processes import *
from brainvisa import registration

name = '16 Concatenate meshes'
userlevel = 2

signature = Signature(
  'LeftWhite', ReadDiskItem('AimsWhite', 'Aims mesh formats',
                            requiredAttributes = {'side' : 'left'}),
  'RightWhite', ReadDiskItem('AimsWhite', 'Aims mesh formats',
                             requiredAttributes = {'side' : 'right'}),
  'LeftPial', ReadDiskItem('AimsPial', 'Aims mesh formats',
                           requiredAttributes = {'side' : 'left'}),
  'RightPial', ReadDiskItem('AimsPial', 'Aims mesh formats',
                            requiredAttributes = {'side' : 'right'}),
  'LeftInflatedWhite', ReadDiskItem('AimsInflatedWhite', 'Aims mesh formats',
                                    requiredAttributes = {'side' : 'left'}),
  'RightInflatedWhite', ReadDiskItem('AimsInflatedWhite', 'Aims mesh formats',
                                     requiredAttributes = {'side' : 'right'}),

  'BothWhite', WriteDiskItem('AimsBothWhite', 'Aims mesh formats'),
  'BothPial', WriteDiskItem('AimsBothPial', 'Aims mesh formats'),
  'BothInflated', WriteDiskItem('AimsBothInflatedWhite', 'Aims mesh formats'),
  )

def initialization(self):
  self.linkParameters('RightWhite', 'LeftWhite')
  self.linkParameters('LeftPial', 'LeftWhite')
  self.linkParameters('RightPial', 'LeftWhite')
  self.linkParameters('LeftInflatedWhite', 'LeftWhite')
  self.linkParameters('RightInflatedWhite', 'LeftWhite')
  self.linkParameters('BothWhite', 'LeftWhite')
  self.linkParameters('BothPial', 'LeftWhite')
  self.linkParameters('BothInflated', 'LeftWhite')


  
def execution(self, context):
  context.write(self.BothWhite.fullPath())
  context.system( 'AimsZCat', '-i', self.LeftWhite.fullPath(),
                  self.RightWhite.fullPath(), '-o',
                  self.BothWhite.fullPath())

  context.write(self.BothPial.fullPath())
  context.system( 'AimsZCat', '-i', self.LeftPial.fullPath(),
                  self.RightPial.fullPath(), '-o',
                  self.BothPial.fullPath())

  context.write(self.BothInflated.fullPath())
  context.system( 'AimsZCat', '-i', self.LeftInflatedWhite.fullPath(),
                  self.RightInflatedWhite.fullPath(), '-o',
                  self.BothInflated.fullPath())

  tm = registration.getTransformationManager()
  tm.copyReferential( self.LeftWhite, self.BothWhite )
  tm.copyReferential( self.LeftPial, self.BothPial )
  tm.copyReferential( self.LeftInflatedWhite, self.BothInflated )
