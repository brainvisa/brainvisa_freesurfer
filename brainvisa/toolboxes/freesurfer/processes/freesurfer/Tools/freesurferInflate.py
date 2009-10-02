from neuroProcesses import *

name = '15 Meshes inflate'
userlevel = 2

signature = Signature(
  'White', ReadDiskItem('AimsWhite', 'MESH mesh'),
  'InflatedWhite', WriteDiskItem('AimsInflatedWhite', 'MESH mesh'),
  'InflatedWhiteCurvTex', WriteDiskItem('AimsInflatedWhite', 'Texture'),
  )

def initialization(self):
  self.linkParameters('White', 'White')
  self.linkParameters('InflatedWhite', 'White')
  self.linkParameters('InflatedWhiteCurvTex', 'White')

  
def execution(self, context):
  context.write(self.White.fullPath())
  context.system( 'AimsInflate', '-i', self.White.fullPath(), '-o',
                  self.InflatedWhite.fullPath(), '-c',
                  self.InflatedWhiteCurvTex.fullPath())
