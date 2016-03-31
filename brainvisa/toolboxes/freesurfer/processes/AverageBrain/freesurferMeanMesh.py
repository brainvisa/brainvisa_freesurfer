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
from brainvisa.processes import Signature, ReadDiskItem, WriteDiskItem, ListOf
from brainvisa.group_utils import Subject

# soma module
from soma.minf.api import registerClass, readMinf
from soma.path import find_in_path


#----------------------------Header--------------------------------------------


name = "2 Average brain mesh"
userLevel = 1

signature = Signature(
    # input
    "group", ReadDiskItem("Freesurfer Group definition", "XML"),
    "individual_rhmeshes", ListOf(
        ReadDiskItem("AimsWhite", "Aims mesh formats")),
    "individual_lhmeshes", ListOf(
        ReadDiskItem("AimsWhite", "Aims mesh formats")),

    # outputs
    "LeftAverageMesh", WriteDiskItem("AverageBrainWhite", "Aims mesh formats",
                                     requiredAttributes={"side": "left"}),
    "RightAverageMesh", WriteDiskItem("AverageBrainWhite", "Aims mesh formats",
                                      requiredAttributes={"side": "right"}),
    "BothAverageMesh", WriteDiskItem("BothAverageBrainWhite",
                                     "Aims mesh formats"),
)


#----------------------------Function------------------------------------------


def initialization(self):
    """Defines the link of parameters.
    """
    def link_rmesh(self, dummy):
        """
        """
        list_mesh = []
        registerClass("minf_2.0", Subject, "Subject")
        groupOfSubjects = readMinf(self.group.fullPath())
        if self.group:
            atrs = {"side": "right", "_database": self.group.get("_database")}
            for subject in groupOfSubjects:
                mesh = self.signature[
                    "individual_rhmeshes"].contentType.findValue(
                    subject.attributes(), requiredAttributes=atrs)
                if mesh:
                    list_mesh.append(mesh)
            return list_mesh

    def link_lmesh(self, dummy):
        """
        """
        list_mesh = []
        registerClass("minf_2.0", Subject, "Subject")
        groupOfSubjects = readMinf(self.group.fullPath())
        if self.group:
            atrs = {"side": "left", "_database": self.group.get("_database")}
            for subject in groupOfSubjects:
                mesh = self.signature[
                    "individual_lhmeshes"].contentType.findValue(
                    subject.attributes(), requiredAttributes=atrs)
                if mesh:
                    list_mesh.append(mesh)
            return list_mesh

    self.linkParameters("individual_lhmeshes", "group", link_lmesh)
    self.linkParameters("individual_rhmeshes", "group", link_rmesh)
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

    # create the left average mesh
    context.system(
        "python2",
        find_in_path("average_mesh.py"),
        self.individual_lhmeshes,
        self.LeftAverageMesh)


    ###########################################################################
    #                        RIGHT HEMISPHERE (rh)                            #
    ###########################################################################


    # create the right average mesh
    context.system(
        "python2",
        find_in_path("average_mesh.py"),
        self.individual_rhmeshes,
        self.LeftAverageMesh)

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
