from brainvisa.processes import *

name = '17 Concatenate textures'
userlevel = 2

signature = Signature(
  'LeftGyri', ReadDiskItem('ResampledGyri', 'Texture',
                            requiredAttributes = {'side' : 'left'}),
  'RightGyri', ReadDiskItem('ResampledGyri', 'Texture',
                            requiredAttributes = {'side' : 'right'}),

  'LeftSulciGyri', ReadDiskItem('ResampledSulciGyri', 'Texture',
                                 requiredAttributes = {'side' : 'left'}),
  'RightSulciGyri', ReadDiskItem('ResampledSulciGyri', 'Texture',
                                  requiredAttributes = {'side' : 'right'}),

  'Gyri', WriteDiskItem('BothResampledGyri', 'Texture'),
  'SulciGyri', WriteDiskItem('BothResampledSulciGyri', 'Texture'),
  )

def initialization(self):
  self.linkParameters('RightGyri', 'LeftGyri')
  self.linkParameters('LeftSulciGyri', 'LeftGyri')
  self.linkParameters('RightSulciGyri', 'LeftGyri')
  self.linkParameters('Gyri', 'LeftGyri')
  self.linkParameters('SulciGyri', 'LeftGyri')

  
def execution(self, context):
  context.write(self.Gyri.fullPath())
  
  context.system('python', '-c', 'from freesurfer.concatenate_textures import concatenate_textures as f; f(\"%s\", (\"%s\", \"%s\"));'%(self.Gyri.fullPath(), self.LeftGyri.fullPath(), self.RightGyri.fullPath()))

  context.write(self.SulciGyri.fullPath())
  
  context.system('python', '-c', 'from freesurfer.concatenate_textures import concatenate_textures as f; f(\"%s\", (\"%s\", \"%s\"));'%(self.SulciGyri.fullPath(), self.LeftSulciGyri.fullPath(), self.RightSulciGyri.fullPath()))

