# -*- coding: utf-8 -*-

import os
from brainvisa.processes import (Signature, String, Choice, neuroHierarchy,
                                 ReadDiskItem, WriteDiskItem, OpenChoice)
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand

name = "01 Create Freesurfer subject from T1 anatomical image"
userLevel = 1

signature = Signature(
    "RawT1Image", ReadDiskItem(
        "Raw T1 MRI", ["NIFTI-1 image", "GZ Compressed NIFTI-1 image"]),
    "subjectName", String(),
    "database", Choice(),
    "AnatImage", WriteDiskItem("RawFreesurferAnat", "FreesurferMGZ")
)


def initialization(self):
    """
    """
    databases = [h.name for h in neuroHierarchy.hierarchies()
                 if h.fso.name == "freesurfer"]
    self.signature["database"].setChoices(*databases)
    if len(databases) != 0:
        self.database = databases[0]
    else:
        self.signature["database"] = OpenChoice()

    def linkSubjectName(proc, dummy):
        """
        """
        if proc.RawT1Image is not None:
            return os.path.basename(os.path.dirname(os.path.dirname(
                os.path.dirname(proc.RawT1Image.fullName()))))

    def linkAnatImage(proc, dummy):
        """
        """
        if proc.subjectName is not None and proc.database is not None:
            subject = proc.subjectName
            dirname = proc.database
            filename = os.path.join(dirname, subject, "mri/orig/001.mgz")
            return filename

    self.linkParameters("subjectName", "RawT1Image", linkSubjectName)
    self.linkParameters(
        "AnatImage", ("subjectName", "database"), linkAnatImage)
    self.signature["AnatImage"].userLevel = 3


def execution(self, context):
    """
    """
    context.write("Create subject hierarchy and convert image to mgz format.")
    launchFreesurferCommand(context, self.database, "mri_convert",
                            self.RawT1Image, self.AnatImage)
    createdDir = self.database + "/" + self.subjectName
    context.write("Updating database, path = " + createdDir)
    neuroHierarchy.databases.update([createdDir])
