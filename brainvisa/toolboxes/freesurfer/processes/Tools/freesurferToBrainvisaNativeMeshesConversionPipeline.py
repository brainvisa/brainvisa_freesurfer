# -*- coding: utf-8 -*-
from brainvisa.processes import *

name = 'Freesurfer NATIVE meshes To BrainVisa conversion pipeline'
userLevel = 2

signature = Signature(
    'anat', ReadDiskItem('RawFreesurferAnat', 'FreesurferMGZ',
                         enableConversion=False),
    'nu', ReadDiskItem('Nu FreesurferAnat', 'FreesurferMGZ',
                       enableConversion=False),
    'ribbon', ReadDiskItem('Ribbon Freesurfer', 'FreesurferMGZ',
                           requiredAttributes={'side': 'both',
                                               'space': 'freesurfer analysis'},
                           enableConversion=False),

    'leftPial', ReadDiskItem('FreesurferType', 'FreesurferPial',
                             requiredAttributes={'side': 'left'}),
    'leftWhite', ReadDiskItem('FreesurferType', 'FreesurferWhite',
                              requiredAttributes={'side': 'left'}),
    'leftSphereReg', ReadDiskItem('FreesurferType', 'FreesurferSphereReg',
                                  requiredAttributes={'side': 'left'}),

    'rightPial', ReadDiskItem('FreesurferType', 'FreesurferPial',
                              requiredAttributes={'side': 'right'}),
    'rightWhite', ReadDiskItem('FreesurferType', 'FreesurferWhite',
                               requiredAttributes={'side': 'right'}),
    'rightSphereReg', ReadDiskItem('FreesurferType', 'FreesurferSphereReg',
                                   requiredAttributes={'side': 'right'}),

  #'bv_anat', ReadDiskItem('Raw T1 MRI', 'NIFTI-1 image')
)


def initialization(self):
    self.linkParameters('nu', 'anat')
    self.linkParameters('ribbon', 'anat')

    self.linkParameters('leftPial', 'anat')

    self.linkParameters('rightPial', 'anat')

    eNode = SerialExecutionNode(self.name, parameterized=self)

    eNode.addChild('CreateReferential',
                   ProcessExecutionNode('newreferential', optional=1))
    eNode.addDoubleLink('CreateReferential.data', 'anat')

    # 3b
    eNode.addChild('BfreesurferImageToNii',
                   ProcessExecutionNode('freesurferAnatToNii', optional=1))
    eNode.BfreesurferImageToNii.removeLink('nu', 'orig')
    eNode.BfreesurferImageToNii.removeLink('ribbon', 'nu')
    eNode.BfreesurferImageToNii.removeLink('referential', 'raw')

    eNode.addDoubleLink('BfreesurferImageToNii.raw', 'anat')
    eNode.addDoubleLink('BfreesurferImageToNii.nu', 'nu')
    eNode.addDoubleLink('BfreesurferImageToNii.ribbon', 'ribbon')
    eNode.addDoubleLink('BfreesurferImageToNii.referential',
                        'CreateReferential.referential')

    # referential
    eNode.addChild('CreateReferentials',
                   ProcessExecutionNode('AddScannerBasedReferential', optional=1))
    eNode.CreateReferentials.removeLink(
        'referential_volume_input', 'volume_input')
    eNode.addDoubleLink('CreateReferentials.volume_input',
                        'BfreesurferImageToNii.raw_nifti')
    eNode.addDoubleLink('CreateReferentials.referential_volume_input',
                        'CreateReferential.referential')

    # MNI transform
    eNode.addChild('MNI_transformation',
                   ProcessExecutionNode('freesurferAnatToTalairachTransform',
                                        optional=1))
    eNode.addDoubleLink('MNI_transformation.scanner_based_referential',
                        'CreateReferentials.new_referential')

    # meshes referential
    eNode.addChild('CreateMeshesReferential',
                   ProcessExecutionNode('createmeshesreferential', optional=1))
    eNode.addDoubleLink('CreateMeshesReferential.anat',
                        'BfreesurferImageToNii.raw_nifti')

    eNode.addChild('CreateMeshesTransformation',
                   ProcessExecutionNode('freesurferAnatToMeshesTransformation',
                                        optional=1))
    eNode.CreateMeshesTransformation.removeLink(
        'freesurfer_meshes_referential',
                                                'anat')
    eNode.CreateMeshesTransformation.removeLink('anat_referential', 'anat')
    eNode.addDoubleLink('BfreesurferImageToNii.raw_nifti',
                        'CreateMeshesTransformation.anat')
    eNode.addDoubleLink('CreateMeshesReferential.meshes_referential',
                        'CreateMeshesTransformation.freesurfer_meshes_referential')
    eNode.addDoubleLink('CreateReferential.referential',
                        'CreateMeshesTransformation.anat_referential')

    # 4 - Left
    eNode.addChild('LfreesurferConversionMeshToGii',
                   ProcessExecutionNode('freesurferConversionMeshToGii',
                                        optional=1))
    # eNode.LfreesurferConversionMeshToGii.removeLink('White', 'Pial')
    # eNode.LfreesurferConversionMeshToGii.removeLink('SphereReg', 'Pial')
    eNode.LfreesurferConversionMeshToGii.removeLink('meshes_referential',
                                                    'PialGifti')

    eNode.addDoubleLink('LfreesurferConversionMeshToGii.Pial', 'leftPial')
    eNode.addDoubleLink('LfreesurferConversionMeshToGii.White', 'leftWhite')
    eNode.addDoubleLink(
        'LfreesurferConversionMeshToGii.SphereReg', 'leftSphereReg')
    eNode.addDoubleLink('LfreesurferConversionMeshToGii.meshes_referential',
                        'CreateMeshesReferential.meshes_referential')

    # 4  -Right
    eNode.addChild('RfreesurferConversionMeshToGii',
                   ProcessExecutionNode('freesurferConversionMeshToGii',
                                        optional=1))
    # eNode.RfreesurferConversionMeshToGii.removeLink('White', 'Pial')
    # eNode.RfreesurferConversionMeshToGii.removeLink('SphereReg', 'Pial')
    eNode.RfreesurferConversionMeshToGii.removeLink('meshes_referential',
                                                    'PialGifti')

    eNode.addDoubleLink('RfreesurferConversionMeshToGii.Pial', 'rightPial')
    eNode.addDoubleLink('RfreesurferConversionMeshToGii.White', 'rightWhite')
    eNode.addDoubleLink(
        'RfreesurferConversionMeshToGii.SphereReg', 'rightSphereReg')
    eNode.addDoubleLink('RfreesurferConversionMeshToGii.meshes_referential',
                        'CreateMeshesReferential.meshes_referential')
    # 5  -Left
    eNode.addChild('LConversionMeshes',
                   ProcessExecutionNode(
                       'Conversion of native (unresampled) meshes to aims referential',
                                        optional=1))
    eNode.LConversionMeshes.removeLink('bv_anat', 'PialMesh')
    # eNode.LConversionMeshes.removeLink('WhiteMesh', 'PialMesh')
    eNode.addDoubleLink('LConversionMeshes.PialMesh',
                        'LfreesurferConversionMeshToGii.PialGifti')
    eNode.addDoubleLink('LConversionMeshes.WhiteMesh',
                        'LfreesurferConversionMeshToGii.WhiteGifti')
    eNode.addDoubleLink(
        'LConversionMeshes.bv_anat', 'BfreesurferImageToNii.raw_nifti')

    # 5  -Right
    eNode.addChild('RConversionMeshes',
                   ProcessExecutionNode(
                       'Conversion of native (unresampled) meshes to aims referential',
                                        optional=1))
    eNode.RConversionMeshes.removeLink('bv_anat', 'PialMesh')
    eNode.RConversionMeshes.removeLink('WhiteMesh', 'PialMesh')
    eNode.addDoubleLink('RConversionMeshes.PialMesh',
                        'RfreesurferConversionMeshToGii.PialGifti')
    eNode.addDoubleLink('RConversionMeshes.WhiteMesh',
                        'RfreesurferConversionMeshToGii.WhiteGifti')
    eNode.addDoubleLink(
        'RConversionMeshes.bv_anat', 'BfreesurferImageToNii.raw_nifti')

    # 18
    self.setExecutionNode(eNode)
