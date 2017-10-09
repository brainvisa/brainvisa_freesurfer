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
)

def initialization(self):
    self.linkParameters('RightGyri', 'LeftGyri')
    self.linkParameters('LeftSulciGyri', 'LeftGyri')
    self.linkParameters('RightSulciGyri', 'LeftGyri')
    self.linkParameters('Gyri', 'LeftGyri')
    self.linkParameters('SulciGyri', 'LeftGyri')
    self.setOptional('LeftGyri', 'RightGyri', 'LeftSulciGyri', 'RightSulciGyri',
                    'Gyri', 'SulciGyri')

  
def execution(self, context):
    if self.Gyri is not None:
        if self.LeftGyri is not None and self.RightGyri is not None:
            context.write(self.Gyri.fullPath())
            context.pythonSystem(
                '-c',
                'from freesurfer.concatenate_textures import concatenate_textures as f; f(\"%s\", \"%s\", \"%s\");'
                % (self.Gyri.fullPath(), self.LeftGyri.fullPath(),
                   self.RightGyri.fullPath()))
        else:
            raise ValueError('Gyri can only be written if LeftGyri and '
                             'RightGyri are present')


    if self.SulciGyri is not None:
        if self.LeftSulciGyri is not None and self.RightSulciGyri is not None:
            context.write(self.SulciGyri.fullPath())

            context.pythonSystem(
                '-c',
                'from freesurfer.concatenate_textures import concatenate_textures as f; f(\"%s\", \"%s\", \"%s\");'
                % (self.SulciGyri.fullPath(), self.LeftSulciGyri.fullPath(),
                   self.RightSulciGyri.fullPath()))
        else:
            raise ValueError('SulciGyri can only be written if LeftSulciGyri '
                             'and RightSulciGyri are present')

