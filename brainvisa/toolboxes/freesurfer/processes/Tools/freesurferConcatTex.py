# -*- coding: utf-8 -*-
import os, sys
from brainvisa.processes import *

name = 'Concatenate textures'
userlevel = 2

signature = Signature(
    'LeftGyri', ReadDiskItem('ResampledGyri', 'Aims Texture formats',
                             requiredAttributes = {'side' : 'left'}),
    'RightGyri', ReadDiskItem('ResampledGyri', 'Aims Texture formats',
                              requiredAttributes = {'side' : 'right'}),

    'LeftSulciGyri', ReadDiskItem('ResampledSulciGyri', 'Aims Texture formats',
                                  requiredAttributes = {'side' : 'left'}),
    'RightSulciGyri', ReadDiskItem('ResampledSulciGyri', 'Aims Texture formats',
                                   requiredAttributes = {'side' : 'right'}),

    'Gyri', WriteDiskItem('BothResampledGyri', 'Aims Texture formats'),
    'SulciGyri', WriteDiskItem('BothResampledSulciGyri',
                               'Aims Texture formats'),
    'hemi_order', Choice(('left-right', 0), ('right-left', 1)),
)

def initialization(self):
    self.linkParameters('RightGyri', 'LeftGyri')
    self.linkParameters('LeftSulciGyri', 'LeftGyri')
    self.linkParameters('RightSulciGyri', 'LeftGyri')
    self.linkParameters('Gyri', 'LeftGyri')
    self.linkParameters('SulciGyri', 'LeftGyri')
    self.setOptional('LeftGyri', 'RightGyri', 'LeftSulciGyri', 'RightSulciGyri',
                     'Gyri', 'SulciGyri')
    self.hemi_order = 0


def execution(self, context):
    if self.Gyri is not None:
        if self.LeftGyri is not None and self.RightGyri is not None:
            context.write(self.Gyri.fullPath())
            if self.hemi_order == 0:
                first = self.LeftGyri
                second = self.RightGyri
            else:
                first = self.RightGyri
                second = self.LeftGyri
            context.pythonSystem(
                '-c',
                'from freesurfer.concatenate_textures import concatenate_textures as f; f(\"%s\", \"%s\", \"%s\");'
                % (self.Gyri.fullPath(), first.fullPath(),
                   second.fullPath()))
        else:
            raise ValueError('Gyri can only be written if LeftGyri and '
                             'RightGyri are present')


    if self.SulciGyri is not None:
        if self.LeftSulciGyri is not None and self.RightSulciGyri is not None:
            context.write(self.SulciGyri.fullPath())

            if self.hemi_order == 0:
                first = self.LeftSulciGyri
                second = self.RightSulciGyri
            else:
                first = self.RightSulciGyri
                second = self.LeftSulciGyri
            context.pythonSystem(
                '-c',
                'from freesurfer.concatenate_textures import concatenate_textures as f; f(\"%s\", \"%s\", \"%s\");'
                % (self.SulciGyri.fullPath(), first.fullPath(),
                   second.fullPath()))
        else:
            raise ValueError('SulciGyri can only be written if LeftSulciGyri '
                             'and RightSulciGyri are present')

