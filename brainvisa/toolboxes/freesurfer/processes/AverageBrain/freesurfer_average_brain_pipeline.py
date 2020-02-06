#
# This software and supporting documentation are distributed by CEA/NeuroSpin,
# Batiment 145, 91191 Gif-sur-Yvette cedex, France. This software is governed
# by the CeCILL license version 2 under French law and abiding by the rules of
# distribution of free software. You can  use, modify and/or redistribute the
# software under the terms of the CeCILL license version 2 as circulated by
# CEA, CNRS and INRIA at the following URL "http://www.cecill.info".
#

"""
This script does the following:
* defines a Brainvisa pipeline
    - the parameters of a pipeline (Signature),
    - the linked parameters between processes.
* provides the average brain (mesh and texture) pipeline.

Main dependencies: axon python API.
"""

#----------------------------Imports-------------------------------------------


# axon python API modules
from brainvisa.processes import Signature, ReadDiskItem, WriteDiskItem, \
    ListOf, SerialExecutionNode, ProcessExecutionNode


#----------------------------Header--------------------------------------------


name = "FreeSurfer Average Brain Pipeline"
userLevel = 0


signature = Signature(
    "list_of_subjects", ListOf(ReadDiskItem("Subject", "Directory")),
    "group_definition", WriteDiskItem("Freesurfer Group definition", "XML"),
)


#----------------------------Pipeline------------------------------------------


def initialization(self):
    """Provides link of parameters
    """
    # define the main node of a pipeline
    eNode = SerialExecutionNode(self.name, parameterized=self)

    #
    # link of parameters for the "Average brain mesh" process          #
    #

    eNode.addChild("create_fsgroup",
                   ProcessExecutionNode(
                       "freesurferCreateGroup", optional=1))

    eNode.addDoubleLink("create_fsgroup.list_of_subjects", "list_of_subjects")
    eNode.addDoubleLink("create_fsgroup.group_definition", "group_definition")

    #
    # link of parameters for the "Average brain mesh" process          #
    #

    eNode.addChild("average_mesh",
                   ProcessExecutionNode(
                       "freesurferMeanMesh", optional=1))

    eNode.addDoubleLink("average_mesh.group", "group_definition")

    #
    # link of parameters for the "Average gyri texture" process         #
    #

    eNode.addChild("average_texture",
                   ProcessExecutionNode(
                       "freesurferMeanGyriTexture", optional=1))

    eNode.addDoubleLink("average_texture.group_freesurfer", "group_definition")

    self.setExecutionNode(eNode)
