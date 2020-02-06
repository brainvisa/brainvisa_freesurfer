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
* provides create a FreeSurfer group.

Main dependencies: axon python API.
"""

#----------------------------Imports-------------------------------------------


# axon python API modules
from brainvisa.processes import Signature, ListOf, ReadDiskItem, WriteDiskItem


#----------------------------Header--------------------------------------------


name = "1 Creation of a group of subject"
userLevel = 1

signature = Signature(
    "list_of_subjects", ListOf(ReadDiskItem("Subject", "Directory")),
    "group_definition", WriteDiskItem("Freesurfer Group definition", "XML"),
)


#----------------------------Functions-----------------------------------------


def execution(self, context):
    context.runProcess(
        "createGroup", self.list_of_subjects, self.group_definition)
