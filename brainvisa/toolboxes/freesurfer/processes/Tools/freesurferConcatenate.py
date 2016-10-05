# -*- coding: utf-8 -*-
from brainvisa.processes import *
from brainvisa import registration

name = 'Concatenate meshes'
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
    'LeftInflatedWhite_sequence',
    ReadDiskItem('AimsInflatedWhite', 'Aims mesh formats',
                 requiredAttributes = {'side': 'left', 'time_sequence': 'Yes'}),
    'RightInflatedWhite_sequence',
    ReadDiskItem('AimsInflatedWhite', 'Aims mesh formats',
                 requiredAttributes = {'side': 'right',
                                       'time_sequence': 'Yes'}),

    'BothWhite', WriteDiskItem('AimsBothWhite', 'Aims mesh formats'),
    'BothPial', WriteDiskItem('AimsBothPial', 'Aims mesh formats'),
    'BothInflated', WriteDiskItem('AimsBothInflatedWhite', 'Aims mesh formats'),
    'BothInflated_sequence',
    WriteDiskItem('AimsBothInflatedWhite', 'Aims mesh formats',
                  requiredAttributes={'time_sequence': 'Yes'}),
)

def initialization(self):
    self.linkParameters('RightWhite', 'LeftWhite')
    self.linkParameters('LeftPial', 'LeftWhite')
    self.linkParameters('RightPial', 'LeftWhite')
    self.linkParameters('LeftInflatedWhite', 'LeftWhite')
    self.linkParameters('RightInflatedWhite', 'LeftWhite')
    self.linkParameters('LeftInflatedWhite_sequence', 'LeftInflatedWhite')
    self.linkParameters('RightInflatedWhite_sequence', 'RightInflatedWhite')
    self.linkParameters('BothWhite', 'LeftWhite')
    self.linkParameters('BothPial', 'LeftWhite')
    self.linkParameters('BothInflated', 'LeftWhite')
    self.linkParameters('BothInflated_sequence', 'BothInflated')
    self.setOptional('LeftInflatedWhite_sequence',
                     'RightInflatedWhite_sequence',
                     'BothInflated_sequence')


def execution(self, context):
    context.write(self.BothWhite.fullPath())
    context.system('AimsZCat', '-i', self.LeftWhite.fullPath(),
                   self.RightWhite.fullPath(), '-o',
                   self.BothWhite.fullPath())

    context.write(self.BothPial.fullPath())
    context.system('AimsZCat', '-i', self.LeftPial.fullPath(),
                   self.RightPial.fullPath(), '-o',
                   self.BothPial.fullPath())

    context.write(self.BothInflated.fullPath())
    context.system('AimsZCat', '-i', self.LeftInflatedWhite.fullPath(),
                   self.RightInflatedWhite.fullPath(), '-o',
                   self.BothInflated.fullPath())

    tm = registration.getTransformationManager()
    tm.copyReferential(self.LeftWhite, self.BothWhite)
    tm.copyReferential(self.LeftPial, self.BothPial)
    tm.copyReferential(self.LeftInflatedWhite, self.BothInflated)

    if self.LeftInflatedWhite_sequence is not None \
            and self.RightInflatedWhite_sequence is not None \
            and self.BothInflated_sequence is not None \
            and self.LeftInflatedWhite_sequence.isReadable() \
            and self.RightInflatedWhite_sequence.isReadable():
        context.system('AimsZCat',
                       '-i', self.LeftInflatedWhite_sequence.fullPath(),
                       self.RightInflatedWhite_sequence.fullPath(),
                       '-o', self.BothInflated_sequence.fullPath())
        tm.copyReferential(self.LeftInflatedWhite_sequence,
                           self.BothInflated_sequence)
