from brainvisa.processes import *

name = '16 Concatenate meshes'
userlevel = 2

signature = Signature(
  'LeftWhite', ReadDiskItem('AimsWhite', 'MESH mesh',
                            requiredAttributes = {'side' : 'left'}),
  'RightWhite', ReadDiskItem('AimsWhite', 'MESH mesh',
                             requiredAttributes = {'side' : 'right'}),
  'LeftPial', ReadDiskItem('AimsPial', 'MESH mesh',
                           requiredAttributes = {'side' : 'left'}),
  'RightPial', ReadDiskItem('AimsPial', 'MESH mesh',
                            requiredAttributes = {'side' : 'right'}),
  'LeftInflatedWhite', ReadDiskItem('AimsInflatedWhite', 'MESH mesh',
                                    requiredAttributes = {'side' : 'left'}),
  'RightInflatedWhite', ReadDiskItem('AimsInflatedWhite', 'MESH mesh',
                                     requiredAttributes = {'side' : 'right'}),

  'BothWhite', WriteDiskItem('AimsBothWhite', 'MESH mesh'),
  'BothPial', WriteDiskItem('AimsBothPial', 'MESH mesh'),
  'BothInflated', WriteDiskItem('AimsBothInflatedWhite', 'MESH mesh'),
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
