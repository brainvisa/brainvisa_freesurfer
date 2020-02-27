# -*- coding: utf-8 -*-
from __future__ import absolute_import
from brainvisa.processes import (Signature, ReadDiskItem, Choice, OpenChoice,
                                 SerialExecutionNode, ProcessExecutionNode,
                                 neuroHierarchy)
from freesurfer.brainvisaFreesurfer import testFreesurferCommand

name = "Freesurfer / BrainVisa full pipeline"
userLevel = 0


def validation():
    testFreesurferCommand()

signature = Signature(
    "RawT1Image", ReadDiskItem(
        "Raw T1 MRI", ["NIFTI-1 image", "GZ Compressed NIFTI-1 image"]),
    "database", Choice(),
)


def initialization(self):

    eNode = SerialExecutionNode(self.name, parameterized=self)

    #
    # 01 Create Freesurfer subject from T1 anatomical image         #
    #

    eNode.addChild(
        "FreeSurfer01",
        ProcessExecutionNode("freesurferCreateSubject", optional=1))

    eNode.addDoubleLink("FreeSurfer01.RawT1Image", "RawT1Image")

    eNode.addDoubleLink("FreeSurfer01.database", "database")

    databases = [h.name for h in neuroHierarchy.hierarchies()
                 if h.fso.name == "freesurfer"]
    self.signature["database"].setChoices(*databases)
    if len(databases) != 0:
        self.database = databases[0]
    else:
        self.signature["database"] = OpenChoice()

    #
    # 02 Launch Freesurfer full pipeline recon-all                 #
    #

    eNode.addChild(
        "FreeSurfer02",
        ProcessExecutionNode("freesurferPipeline", optional=1))

    eNode.addDoubleLink("FreeSurfer02.AnatImage", "FreeSurfer01.AnatImage")

    #
    # FreeSurfer outputs To BrainVisa conversion pipeline              #
    #

    eNode.addChild(
        "FreeSurferPipeline",
        ProcessExecutionNode("freesurferToBrainvisaConversionPipeline",
                             optional=1))

    eNode.addDoubleLink("FreeSurferPipeline.anat", "FreeSurfer02.AnatImage")

    eNode.FreeSurferPipeline.removeLink("nu", "anat")

    eNode.FreeSurferPipeline.removeLink("ribbon", "anat")

    eNode.FreeSurferPipeline.removeLink("leftPial", "anat")
    eNode.FreeSurferPipeline.removeLink("leftCurv", "anat")

    eNode.FreeSurferPipeline.removeLink("rightPial", "anat")
    eNode.FreeSurferPipeline.removeLink("rightCurv", "anat")

    eNode.addDoubleLink("FreeSurferPipeline.nu", "FreeSurfer02.nu")
    eNode.addDoubleLink("FreeSurferPipeline.ribbon", "FreeSurfer02.ribbon")

    # left hemisphere
    eNode.addDoubleLink(
        "FreeSurferPipeline.leftPial", "FreeSurfer02.leftPial")

    eNode.addDoubleLink(
        "FreeSurferPipeline.leftWhite", "FreeSurfer02.leftWhite")

    eNode.addDoubleLink(
        "FreeSurferPipeline.leftSphereReg", "FreeSurfer02.leftSphereReg")

    eNode.addDoubleLink(
        "FreeSurferPipeline.leftThickness", "FreeSurfer02.leftThickness")

    eNode.addDoubleLink(
        "FreeSurferPipeline.leftCurv", "FreeSurfer02.leftCurv")

    eNode.addDoubleLink(
        "FreeSurferPipeline.leftAvgCurv", "FreeSurfer02.leftAvgCurv")

    eNode.addDoubleLink(
        "FreeSurferPipeline.leftCurvPial", "FreeSurfer02.leftCurvPial")

    eNode.addDoubleLink(
        "FreeSurferPipeline.leftGyri", "FreeSurfer02.leftGyri")

    eNode.addDoubleLink(
        "FreeSurferPipeline.leftSulciGyri", "FreeSurfer02.leftSulciGyri")

    # right hemisphere
    eNode.addDoubleLink(
        "FreeSurferPipeline.rightPial", "FreeSurfer02.rightPial")

    eNode.addDoubleLink(
        "FreeSurferPipeline.rightWhite", "FreeSurfer02.rightWhite")

    eNode.addDoubleLink(
        "FreeSurferPipeline.rightSphereReg", "FreeSurfer02.rightSphereReg")

    eNode.addDoubleLink(
        "FreeSurferPipeline.rightThickness", "FreeSurfer02.rightThickness")

    eNode.addDoubleLink(
        "FreeSurferPipeline.rightCurv", "FreeSurfer02.rightCurv")

    eNode.addDoubleLink(
        "FreeSurferPipeline.rightAvgCurv", "FreeSurfer02.rightAvgCurv")

    eNode.addDoubleLink(
        "FreeSurferPipeline.rightCurvPial", "FreeSurfer02.rightCurvPial")

    eNode.addDoubleLink(
        "FreeSurferPipeline.rightGyri", "FreeSurfer02.rightGyri")

    eNode.addDoubleLink(
        "FreeSurferPipeline.rightSulciGyri", "FreeSurfer02.rightSulciGyri")

    self.setExecutionNode(eNode)
