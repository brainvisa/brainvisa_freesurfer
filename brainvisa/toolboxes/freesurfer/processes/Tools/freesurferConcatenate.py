# -*- coding: utf-8 -*-
from brainvisa.processes import *
from brainvisa import registration

name = 'Concatenate meshes'
userlevel = 2

signature = Signature(
    'LeftWhite', ReadDiskItem('AimsWhite', 'Aims mesh formats',
                              requiredAttributes={'side': 'left'}),
    'RightWhite', ReadDiskItem('AimsWhite', 'Aims mesh formats',
                               requiredAttributes={'side': 'right'}),
    'LeftPial', ReadDiskItem('AimsPial', 'Aims mesh formats',
                             requiredAttributes={'side': 'left'}),
    'RightPial', ReadDiskItem('AimsPial', 'Aims mesh formats',
                              requiredAttributes={'side': 'right'}),
    'LeftInflatedWhite', ReadDiskItem('AimsInflatedWhite', 'Aims mesh formats',
                                      requiredAttributes={'side': 'left'}),
    'RightInflatedWhite', ReadDiskItem('AimsInflatedWhite', 'Aims mesh formats',
                                       requiredAttributes={
                                           'side': 'right'}),
    'LeftInflatedWhite_sequence',
    ReadDiskItem('AimsInflatedWhite', 'Aims mesh formats',
                 requiredAttributes={
                     'side': 'left', 'time_sequence': 'Yes'}),
    'RightInflatedWhite_sequence',
    ReadDiskItem('AimsInflatedWhite', 'Aims mesh formats',
                 requiredAttributes={'side': 'right',
                                     'time_sequence': 'Yes'}),

    'BothWhite', WriteDiskItem('AimsBothWhite', 'Aims mesh formats'),
    'BothPial', WriteDiskItem('AimsBothPial', 'Aims mesh formats'),
    'BothInflated', WriteDiskItem(
        'AimsBothInflatedWhite', 'Aims mesh formats'),
    'BothInflated_sequence',
    WriteDiskItem('AimsBothInflatedWhite', 'Aims mesh formats',
                  requiredAttributes={'time_sequence': 'Yes'}),
    'hemi_order', Choice(('left-right', 0), ('right-left', 1)),
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
    self.setOptional('LeftWhite', 'RightWhite', 'LeftPial', 'RightPial',
                     'LeftInflatedWhite', 'RightInflatedWhite',
                     'LeftInflatedWhite_sequence',
                     'RightInflatedWhite_sequence', 'BothWhite', 'BothPial',
                     'BothInflated', 'BothInflated_sequence')
    self.hemi_order = 0


def execution(self, context):
    tm = registration.getTransformationManager()
    if self.BothWhite is not None:
        if self.LeftWhite is not None and self.RightWhite is not None:
            context.write(self.BothWhite.fullPath())
            if self.hemi_order == 0:
                context.system('AimsZCat', '-i', self.LeftWhite.fullPath(),
                               self.RightWhite.fullPath(), '-o',
                               self.BothWhite.fullPath())
            else:
                context.system('AimsZCat', '-i', self.RightWhite.fullPath(),
                               self.LeftWhite.fullPath(), '-o',
                               self.BothWhite.fullPath())
            tm.copyReferential(self.LeftWhite, self.BothWhite)
        else:
            raise ValueError('BothWhite can only be written if LeftWhite and '
                             'RightWhite are present')

    if self.BothPial is not None:
        if self.LeftPial is not None and self.RightPial is not None:
            context.write(self.BothPial.fullPath())
            if self.hemi_order == 0:
                context.system('AimsZCat', '-i', self.LeftPial.fullPath(),
                               self.RightPial.fullPath(), '-o',
                               self.BothPial.fullPath())
            else:
                context.system('AimsZCat', '-i', self.RightPial.fullPath(),
                               self.LeftPial.fullPath(), '-o',
                               self.BothPial.fullPath())
            tm.copyReferential(self.LeftPial, self.BothPial)
        else:
            raise ValueError('BothPial can only be written if LeftPial and '
                             'RightPial are present')

    if self.BothInflated is not None:
        if self.LeftInflatedWhite is not None \
                and self.RightInflatedWhite is not None:
            context.write(self.BothInflated.fullPath())
            if self.hemi_order == 0:
                context.system('AimsZCat', '-i',
                               self.LeftInflatedWhite.fullPath(),
                               self.RightInflatedWhite.fullPath(), '-o',
                               self.BothInflated.fullPath())
            else:
                context.system('AimsZCat', '-i',
                               self.RightInflatedWhite.fullPath(),
                               self.LeftInflatedWhite.fullPath(), '-o',
                               self.BothInflated.fullPath())
            tm.copyReferential(self.LeftInflatedWhite, self.BothInflated)
        else:
            raise ValueError('BothInflated can only be written if '
                             'LeftInflatedWhite and RightInflatedWhite are '
                             'present')

    if self.LeftInflatedWhite_sequence is not None \
            and self.RightInflatedWhite_sequence is not None \
            and self.BothInflated_sequence is not None \
            and self.LeftInflatedWhite_sequence.isReadable() \
            and self.RightInflatedWhite_sequence.isReadable():
        if self.hemi_order == 0:
            context.system('AimsZCat',
                           '-i', self.LeftInflatedWhite_sequence.fullPath(),
                           self.RightInflatedWhite_sequence.fullPath(),
                           '-o', self.BothInflated_sequence.fullPath())
        else:
            context.system('AimsZCat',
                           '-i', self.RightInflatedWhite_sequence.fullPath(),
                           self.LeftInflatedWhite_sequence.fullPath(),
                           '-o', self.BothInflated_sequence.fullPath())
        tm.copyReferential(self.LeftInflatedWhite_sequence,
                           self.BothInflated_sequence)
