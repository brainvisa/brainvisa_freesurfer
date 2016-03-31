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

Main dependencies: axon python API.
"""

#----------------------------Imports-------------------------------------------


# axon python API module
from brainvisa.processes import Signature, ReadDiskItem, WriteDiskItem, \
    ValidationError, ListOf
from brainvisa.group_utils import Subject
from soma.minf.api import registerClass, readMinf

# soma-base module
from soma.path import find_in_path


#----------------------------Header--------------------------------------------


def validation():
    """This function is executed at BrainVisa startup when the process is
    loaded. It checks some conditions for the process to be available.
    """
    if not find_in_path("constelGyriTextureCleaningIsolatedVertices.py"):
        raise ValidationError(
            "Please make sure that constel module is installed.")


name = "3 Average Gyri Texture"
userLevel = 1

# Argument declaration
signature = Signature(
    # inputs
    "group_freesurfer", ReadDiskItem("Freesurfer Group definition", "XML"),
    "mesh", ReadDiskItem("BothAverageBrainWhite", "Aims mesh formats"),
    "gyri_segmentations", ListOf(
        ReadDiskItem("BothResampledGyri", "Aims texture formats")),

    # outputs
    "avg_gyri_texture", WriteDiskItem(
        "BothAverageResampledGyri", "Aims texture formats"),
)


#----------------------------Functions-----------------------------------------


# Default values
def initialization(self):
    """Defines the link of parameters.
    """
    def link_gyriseg(self, dummy):
        """
        """
        gyri_seg = []
        registerClass("minf_2.0", Subject, "Subject")
        groupOfSubjects = readMinf(self.group_freesurfer.fullPath())
        if self.group_freesurfer:
            atrs = {"_database": self.group_freesurfer.get("_database")}
            for subject in groupOfSubjects:
                seg = self.signature[
                    "gyri_segmentations"].contentType.findValue(
                    subject.attributes(), requiredAttributes=atrs)
                if seg:
                    gyri_seg.append(seg)
            return gyri_seg

    self.linkParameters("mesh", "group_freesurfer")
    self.linkParameters("avg_gyri_texture", "group_freesurfer")
    self.linkParameters("gyri_segmentations", "group_freesurfer", link_gyriseg)


def execution(self, context):
    """
    """
    # create the average texture
    context.system('python2',
                   find_in_path('freesurferAvgGyriTexture.py'),
                   self.gyri_segmentations,
                   self.avg_gyri_texture)

    # compute the connected component
    context.system(
        "python",
        find_in_path("constelGyriTextureCleaningIsolatedVertices.py"),
        self.avg_gyri_texture,
        self.mesh,
        self.avg_gyri_texture
    )
