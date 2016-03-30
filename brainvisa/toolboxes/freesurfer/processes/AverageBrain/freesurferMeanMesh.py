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
* provides create left, right and both average mesh from a group of subjects.

Main dependencies: axon python API.
"""

#----------------------------Imports-------------------------------------------


# axon python API modules
from brainvisa.processes import Signature, ReadDiskItem, WriteDiskItem
from brainvisa.group_utils import Subject

# soma module
from soma.minf.api import registerClass, readMinf


#----------------------------Header--------------------------------------------


name = "2 Average brain mesh"
userLevel = 1

signature = Signature(
    # input
    "group", ReadDiskItem("Freesurfer Group definition", "XML"),

    # outputs
    "LeftAverageMesh", WriteDiskItem("AverageBrainWhite", "Aims mesh formats",
                                     requiredAttributes={"side": "left"}),
    "RightAverageMesh", WriteDiskItem("AverageBrainWhite", "Aims mesh formats",
                                      requiredAttributes={"side": "right"}),
    "BothAverageMesh", WriteDiskItem("BothAverageBrainWhite",
                                     "Aims mesh formats"),
)


#----------------------------Functionc-----------------------------------------


def initialization(self):
    """
    """
    self.linkParameters("LeftAverageMesh", "group")
    self.linkParameters("RightAverageMesh", "group")
    self.linkParameters("BothAverageMesh", "group")


def execution(self, context):
    """
    """
    registerClass("minf_2.0", Subject, "Subject")
    groupOfSubjects = readMinf(self.group.fullPath())

    ###########################################################################
    #                        LEFT HEMISPHERE (lh)                             #
    ###########################################################################

    # list all left meshes
    subjects = []
    rattrs = {"side": "left", "_database": self.group.get("_database")}
    for subject in groupOfSubjects:
        subjects.append(
            ReadDiskItem("AimsWhite", "Aims mesh formats").findValue(
                subject.attributes(), requiredAttributes=rattrs))

    context.write(str([i.fullPath() for i in subjects]))

    # create the left average mesh
    context.system(
        "python2",
        "-c",
        "from freesurfer.average_mesh import average_mesh as f; f(\"%s\", %s);"%(
            self.LeftAverageMesh.fullPath(),
            str([i.fullPath() for i in subjects])))

    ###########################################################################
    #                        RIGHT HEMISPHERE (rh)                            #
    ###########################################################################

    # list all right meshes
    subjects = []
    rattrs = {"side": "right", "_database": self.group.get("_database")}
    for subject in groupOfSubjects:
        subjects.append(
            ReadDiskItem("AimsWhite", "Aims mesh formats").findValue(
                subject.attributes(), requiredAttributes=rattrs))

    context.write(str([i.fullPath() for i in subjects]))

    # create the right average mesh
    context.system(
        "python2",
        "-c",
        "from freesurfer.average_mesh import average_mesh as f; f(\"%s\", %s);"%(
            self.RightAverageMesh.fullPath(),
            str([i.fullPath() for i in subjects])))

    ###########################################################################
    #                        BOTH HEMISPHERE (bh)                             #
    ###########################################################################

    # concatenate the left and right average meshes
    # create the both average mesh
    context.system(
        "AimsZCat",
        "-i", self.LeftAverageMesh.fullPath(),
        self.RightAverageMesh.fullPath(),
        "-o", self.BothAverageMesh.fullPath()
        )
