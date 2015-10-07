#!/usr/bin/env python
###############################################################################
# This software and supporting documentation are distributed by CEA/NeuroSpin,
# Batiment 145, 91191 Gif-sur-Yvette cedex, France. This software is governed
# by the CeCILL license version 2 under French law and abiding by the rules of
# distribution of free software. You can  use, modify and/or redistribute the
# software under the terms of the CeCILL license version 2 as circulated by
# CEA, CNRS and INRIA at the following URL "http://www.cecill.info".
###############################################################################

"""
This script does the following:
* load all the both individual textures to a given freesurfer group
* compute the connected components to delete the isolated points on the average
  texture

Author:
"""

#----------------------------Imports-------------------------------------------


# axon python API module
from brainvisa.processes import Signature, ReadDiskItem, WriteDiskItem, \
    ValidationError
from brainvisa.group_utils import Subject
from soma.minf.api import registerClass, readMinf

# soma-base module
from soma.path import find_in_path


#----------------------------Functions-----------------------------------------


def validation():
    """This function is executed at BrainVisa startup when the process is
    loaded. It checks some conditions for the process to be available.
    """
    if not find_in_path("constelGyriTextureCleaningIsolatedVertices.py"):
        raise ValidationError(
            "Please make sure that constel module is installed.")


name = '3 Average Gyri Texture'
userLevel = 1


# Argument declaration
signature = Signature(
    'group_freesurfer', ReadDiskItem('Freesurfer Group definition', 'XML'),
    'mesh', ReadDiskItem('BothAverageBrainWhite', 'MESH mesh'),
    'avg_gyri_texture', WriteDiskItem('BothAverageResampledGyri',
                                      'aims texture formats'),
)


# Default values
def initialization(self):
    self.linkParameters('mesh', 'group_freesurfer')
    self.linkParameters('avg_gyri_texture', "group_freesurfer')

  
def execution ( self, context ):
    registerClass('minf_2.0', Subject, 'Subject')
    groupOfSubjects = readMinf(self.group_freesurfer.fullPath())
    textures = []
    for subject in groupOfSubjects:
        textures.append(ReadDiskItem(
            'BothResampledGyri', 'Aims texture formats').findValue(
            subject.attributes()))
    context.write(str([i for i in textures]))
  
    cmd_args = []
    for tex in textures:
        cmd_args += ['-i', tex]
    cmd_args += ['-o', self.avg_gyri_texture]
    context.system('python',
                   find_in_path('freesurferAvgGyriTexture.py'), *cmd_args)
    # Computing connected component:
    context.system(
        'python', find_in_path('constelGyriTextureCleaningIsolatedVertices.py'),
        '-i', self.avg_gyri_texture,
        '-m', self.mesh,
        '-o', self.avg_gyri_texture
    )

