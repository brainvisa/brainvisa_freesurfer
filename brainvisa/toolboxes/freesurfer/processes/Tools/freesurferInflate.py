# -*- coding: utf-8 -*-
from brainvisa.processes import *
from brainvisa import registration

name = 'Meshes inflate'
userlevel = 2

signature = Signature(
    'White', ReadDiskItem('AimsWhite', 'Aims mesh formats'),
    'InflatedWhite', WriteDiskItem('AimsInflatedWhite', 'Aims mesh formats'),
    'InflatedWhiteCurvTex', WriteDiskItem('AimsInflatedWhiteCurvTex',
                                          'Aims Texture formats'),
    'save_sequence', Boolean(),
    'InflatedWhite_sequence',
    WriteDiskItem('AimsInflatedWhite', 'Aims mesh formats',
                  requiredAttributes={'time_sequence': 'Yes'}),
)


def initialization(self):
    self.save_sequence = True
    self.setOptional('InflatedWhite_sequence')
    self.linkParameters('InflatedWhite', 'White')
    self.linkParameters('InflatedWhiteCurvTex', 'White')
    self.linkParameters('InflatedWhite_sequence', 'White')


def execution(self, context):
    context.write(self.White.fullPath())
    context.system('AimsInflate', '-i', self.White.fullPath(),
                   '-o', self.InflatedWhite.fullPath(),
                   '-c', self.InflatedWhiteCurvTex.fullPath())
    tm = registration.getTransformationManager()
    tm.copyReferential(self.White, self.InflatedWhite)
    if self.save_sequence:
        context.system('AimsInflate', '-i', self.White.fullPath(),
                      '-o', self.InflatedWhite.fullPath(),
                      '-c', self.InflatedWhiteCurvTex.fullPath(),
                      '-S')
        tm.copyReferential(self.White, self.InflatedWhite_sequence)
