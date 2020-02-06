# -*- coding: utf-8 -*-
from brainvisa.processes import *

name = 'Freesurfer outputs To BrainVisa conversion pipeline'
userLevel = 0

signature = Signature(
    'anat', ReadDiskItem('RawFreesurferAnat', 'FreesurferMGZ',
                         enableConversion=False),
    'icosphere_type', Choice('brainvisa 40k', 'hcp 32k', 'freesurfer ic6 40k'),
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
    'leftThickness', ReadDiskItem('FreesurferType', 'FreesurferThickness',
                                  requiredAttributes={'side': 'left'}),
    'leftCurv', ReadDiskItem('FreesurferType', 'FreesurferCurv',
                             requiredAttributes={'side': 'left'}),
    'leftAvgCurv', ReadDiskItem('FreesurferType', 'FreesurferAvgCurv',
                                requiredAttributes={'side': 'left'}),
    'leftCurvPial', ReadDiskItem('FreesurferType', 'FreesurferCurvPial',
                                 requiredAttributes={'side': 'left'}),
    'leftGyri', ReadDiskItem('FreesurferGyriTexture', 'FreesurferParcellation',
                             requiredAttributes={'side': 'left'}),
    'leftSulciGyri',
            ReadDiskItem(
                'FreesurferSulciGyriTexture', 'FreesurferParcellation',
            requiredAttributes={'side': 'left'}),

    'rightPial', ReadDiskItem('FreesurferType', 'FreesurferPial',
                              requiredAttributes={'side': 'right'}),
    'rightWhite', ReadDiskItem('FreesurferType', 'FreesurferWhite',
                               requiredAttributes={'side': 'right'}),
    'rightSphereReg', ReadDiskItem('FreesurferType', 'FreesurferSphereReg',
                                   requiredAttributes={'side': 'right'}),
    'rightThickness', ReadDiskItem('FreesurferType', 'FreesurferThickness',
                                   requiredAttributes={'side': 'right'}),
    'rightCurv', ReadDiskItem('FreesurferType', 'FreesurferCurv',
                              requiredAttributes={'side': 'right'}),
    'rightAvgCurv', ReadDiskItem('FreesurferType', 'FreesurferAvgCurv',
                                 requiredAttributes={'side': 'right'}),
    'rightCurvPial', ReadDiskItem('FreesurferType', 'FreesurferCurvPial',
                                  requiredAttributes={'side': 'right'}),
    'rightGyri', ReadDiskItem('FreesurferGyriTexture', 'FreesurferParcellation',
                              requiredAttributes={'side': 'right'}),
    'rightSulciGyri',
            ReadDiskItem(
                'FreesurferSulciGyriTexture', 'FreesurferParcellation',
            requiredAttributes={'side': 'right'}),

  #'bv_anat', ReadDiskItem('Raw T1 MRI', 'NIFTI-1 image')
)


def initialization(self):
    self.linkParameters('nu', 'anat')
    self.linkParameters('ribbon', 'anat')

    self.linkParameters('leftPial', 'anat')
    self.linkParameters('leftCurv', 'anat')

    self.linkParameters('rightPial', 'anat')
    self.linkParameters('rightCurv', 'anat')
    self.setOptional('icosphere_type')

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

    pNode = ParallelExecutionNode('lat1', optional=True,
                                  expandedInGui=True)
    eNode.addChild('lat1', pNode)

    # 4 - Left
    slNode = SerialExecutionNode('left', optional=True, expandedInGui=True)
    pNode.addChild('left', slNode)
    slNode.addChild('LfreesurferConversionMeshToGii',
                    ProcessExecutionNode('freesurferConversionMeshToGii',
                                         optional=1))
    # eNode.LfreesurferConversionMeshToGii.removeLink('White', 'Pial')
    # eNode.LfreesurferConversionMeshToGii.removeLink('SphereReg', 'Pial')
    slNode.LfreesurferConversionMeshToGii.removeLink('meshes_referential',
                                                     'PialGifti')

    eNode.addDoubleLink('lat1.left.LfreesurferConversionMeshToGii.Pial',
                        'leftPial')
    eNode.addDoubleLink('lat1.left.LfreesurferConversionMeshToGii.White',
                        'leftWhite')
    eNode.addDoubleLink(
        'lat1.left.LfreesurferConversionMeshToGii.SphereReg', 'leftSphereReg')
    eNode.addDoubleLink(
        'lat1.left.LfreesurferConversionMeshToGii.meshes_referential',
        'CreateMeshesReferential.meshes_referential')

    # 4  -Right
    srNode = SerialExecutionNode('right', optional=True, expandedInGui=True)
    pNode.addChild('right', srNode)
    srNode.addChild('RfreesurferConversionMeshToGii',
                    ProcessExecutionNode('freesurferConversionMeshToGii',
                                         optional=1))
    # eNode.RfreesurferConversionMeshToGii.removeLink('White', 'Pial')
    # eNode.RfreesurferConversionMeshToGii.removeLink('SphereReg', 'Pial')
    srNode.RfreesurferConversionMeshToGii.removeLink('meshes_referential',
                                                     'PialGifti')

    eNode.addDoubleLink(
        'lat1.right.RfreesurferConversionMeshToGii.Pial', 'rightPial')
    eNode.addDoubleLink(
        'lat1.right.RfreesurferConversionMeshToGii.White', 'rightWhite')
    eNode.addDoubleLink(
        'lat1.right.RfreesurferConversionMeshToGii.SphereReg',
        'rightSphereReg')
    eNode.addDoubleLink(
        'lat1.right.RfreesurferConversionMeshToGii.meshes_referential',
        'CreateMeshesReferential.meshes_referential')

    #

    slNode.addChild('CreateMeshesTransformation',
                   ProcessExecutionNode('freesurferAnatToMeshesTransformation',
                                        optional=1))
    slNode.CreateMeshesTransformation.removeLink(
        'freesurfer_meshes_referential', 'anat')
    eNode.addDoubleLink(
        'lat1.left.CreateMeshesTransformation.scanner_based_to_mni',
        'MNI_transformation.transform_to_mni')
    slNode.addDoubleLink('CreateMeshesTransformation.fs_mesh',
                         'LfreesurferConversionMeshToGii.PialGifti')
    slNode.CreateMeshesTransformation.removeLink('anat_referential', 'anat')
    eNode.addDoubleLink('BfreesurferImageToNii.raw_nifti',
                        'lat1.left.CreateMeshesTransformation.anat')
    eNode.addDoubleLink(
        'CreateMeshesReferential.meshes_referential',
        'lat1.left.CreateMeshesTransformation.freesurfer_meshes_referential')
    eNode.addDoubleLink(
        'CreateReferential.referential',
        'lat1.left.CreateMeshesTransformation.anat_referential')

    # 6
    slNode.addChild('LfreesurferIsinComputing',
                    ProcessExecutionNode('freesurferIsinComputing',
                                         optional=1))
    slNode.addDoubleLink('LfreesurferIsinComputing.SphereRegMesh',
                         'LfreesurferConversionMeshToGii.SphereRegGifti')
    eNode.addDoubleLink('icosphere_type',
                        'lat1.left.LfreesurferIsinComputing.icosphere_type')
    srNode.addChild('RfreesurferIsinComputing',
                    ProcessExecutionNode('freesurferIsinComputing',
                                         optional=1))
    srNode.addDoubleLink(
        'RfreesurferIsinComputing.SphereRegMesh',
        'RfreesurferConversionMeshToGii.SphereRegGifti')
    eNode.addDoubleLink('icosphere_type',
                        'lat1.right.RfreesurferIsinComputing.icosphere_type')

    # 7
    slNode.addChild('LfreesurferMeshResampling',
                    ProcessExecutionNode('freesurferMeshResampling',
                                         optional=1))
    slNode.LfreesurferMeshResampling.removeLink('WhiteMesh', 'PialMesh')
    slNode.LfreesurferMeshResampling.removeLink('Isin', 'PialMesh')
    slNode.LfreesurferMeshResampling.removeLink('destination', 'PialMesh')
    slNode.addDoubleLink('LfreesurferMeshResampling.PialMesh',
                         'LfreesurferConversionMeshToGii.PialGifti')
    slNode.addDoubleLink('LfreesurferMeshResampling.WhiteMesh',
                         'LfreesurferConversionMeshToGii.WhiteGifti')
    slNode.addDoubleLink('LfreesurferMeshResampling.destination',
                         'LfreesurferIsinComputing.destination')
    slNode.addDoubleLink('LfreesurferMeshResampling.Isin',
                         'LfreesurferIsinComputing.Isin')
    # destination has already a value in freesurferIsinComputing, so will
    # not propagate automatically at the beginning
    eNode.lat1.left.LfreesurferMeshResampling.setValue(
        'destination', eNode.lat1.left.LfreesurferIsinComputing.destination)

    srNode.addChild('RfreesurferMeshResampling',
                    ProcessExecutionNode('freesurferMeshResampling',
                                         optional=1))
    srNode.RfreesurferMeshResampling.removeLink('WhiteMesh', 'PialMesh')
    srNode.RfreesurferMeshResampling.removeLink('Isin', 'PialMesh')
    srNode.RfreesurferMeshResampling.removeLink('destination', 'PialMesh')
    srNode.addDoubleLink('RfreesurferMeshResampling.PialMesh',
                         'RfreesurferConversionMeshToGii.PialGifti')
    srNode.addDoubleLink('RfreesurferMeshResampling.WhiteMesh',
                         'RfreesurferConversionMeshToGii.WhiteGifti')
    srNode.addDoubleLink('RfreesurferMeshResampling.destination',
                         'RfreesurferIsinComputing.destination')
    srNode.addDoubleLink('RfreesurferMeshResampling.Isin',
                         'RfreesurferIsinComputing.Isin')
    # destination has already a value in freesurferIsinComputing, so will
    # not propagate automatically at the beginning
    eNode.lat1.right.RfreesurferMeshResampling.setValue(
        'destination', eNode.lat1.right.RfreesurferIsinComputing.destination)

    # 8
    slNode.addChild('LfreesurferMeshToAimsRef',
                    ProcessExecutionNode('freesurferMeshToAimsRef',
                                         optional=1))
    slNode.LfreesurferMeshToAimsRef.removeLink('ResampledWhiteMesh',
                                               'ResampledPialMesh')
    slNode.LfreesurferMeshToAimsRef.removeLink('bv_anat', 'ResampledPialMesh')
    slNode.addDoubleLink(
        'LfreesurferMeshToAimsRef.ResampledPialMesh',
        'LfreesurferMeshResampling.ResampledPialMesh')
    slNode.addDoubleLink(
        'LfreesurferMeshToAimsRef.ResampledWhiteMesh',
        'LfreesurferMeshResampling.ResampledWhiteMesh')
    eNode.addDoubleLink('lat1.left.LfreesurferMeshToAimsRef.bv_anat',
                        'BfreesurferImageToNii.raw_nifti')
    eNode.addDoubleLink(
        'lat1.left.LfreesurferMeshToAimsRef.scanner_based_to_mni',
        'MNI_transformation.transform_to_mni')

    srNode.addChild('RfreesurferMeshToAimsRef',
                    ProcessExecutionNode('freesurferMeshToAimsRef',
                                         optional=1))
    srNode.RfreesurferMeshToAimsRef.removeLink('bv_anat', 'ResampledPialMesh')
    srNode.addDoubleLink(
        'RfreesurferMeshToAimsRef.ResampledPialMesh',
        'RfreesurferMeshResampling.ResampledPialMesh')
    srNode.addDoubleLink(
        'RfreesurferMeshToAimsRef.ResampledWhiteMesh',
        'RfreesurferMeshResampling.ResampledWhiteMesh')
    eNode.addDoubleLink('lat1.right.RfreesurferMeshToAimsRef.bv_anat',
                        'BfreesurferImageToNii.raw_nifti')
    eNode.addDoubleLink(
        'lat1.right.RfreesurferMeshToAimsRef.scanner_based_to_mni',
        'MNI_transformation.transform_to_mni')

    # 9/10
    slNode.addChild('LfreesurferLabelToAimsTexture',
                    ProcessExecutionNode('freesurferLabelToAimsTexture',
                                         optional=1))
    slNode.addDoubleLink('LfreesurferLabelToAimsTexture.WhiteMesh',
                         'LfreesurferConversionMeshToGii.WhiteGifti')
    eNode.addDoubleLink(
        'lat1.left.LfreesurferLabelToAimsTexture.Gyri', 'leftGyri')
    eNode.addDoubleLink('lat1.left.LfreesurferLabelToAimsTexture.SulciGyri',
                        'leftSulciGyri')

    srNode.addChild('RfreesurferLabelToAimsTexture',
                    ProcessExecutionNode('freesurferLabelToAimsTexture',
                                         optional=1))
    srNode.addDoubleLink('RfreesurferLabelToAimsTexture.WhiteMesh',
                         'RfreesurferConversionMeshToGii.WhiteGifti')
    eNode.addDoubleLink(
        'lat1.right.RfreesurferLabelToAimsTexture.Gyri', 'rightGyri')
    eNode.addDoubleLink('lat1.right.RfreesurferLabelToAimsTexture.SulciGyri',
                        'rightSulciGyri')
    # 11
    slNode.addChild('LfreesurferResampleLabels',
                    ProcessExecutionNode('freesurferResampleLabels',
                                         optional=1))
    slNode.LfreesurferResampleLabels.removeLink('Isin', 'WhiteMesh')
    slNode.LfreesurferResampleLabels.removeLink('Gyri', 'WhiteMesh')
    slNode.LfreesurferResampleLabels.removeLink('SulciGyri', 'WhiteMesh')
    slNode.addDoubleLink('LfreesurferResampleLabels.WhiteMesh',
                         'LfreesurferConversionMeshToGii.WhiteGifti')
    slNode.addDoubleLink('LfreesurferResampleLabels.Isin',
                         'LfreesurferIsinComputing.Isin')
    slNode.addDoubleLink('LfreesurferResampleLabels.Gyri',
                         'LfreesurferLabelToAimsTexture.GyriTexture')
    slNode.addDoubleLink('LfreesurferResampleLabels.SulciGyri',
                         'LfreesurferLabelToAimsTexture.SulciGyriTexture')

    srNode.addChild('RfreesurferResampleLabels',
                     ProcessExecutionNode('freesurferResampleLabels',
                                          optional=1))
    srNode.RfreesurferResampleLabels.removeLink('Isin', 'WhiteMesh')
    srNode.RfreesurferResampleLabels.removeLink('Gyri', 'WhiteMesh')
    srNode.RfreesurferResampleLabels.removeLink('SulciGyri', 'WhiteMesh')
    srNode.addDoubleLink('RfreesurferResampleLabels.WhiteMesh',
                         'RfreesurferConversionMeshToGii.WhiteGifti')
    srNode.addDoubleLink('RfreesurferResampleLabels.Isin',
                         'RfreesurferIsinComputing.Isin')
    srNode.addDoubleLink('RfreesurferResampleLabels.Gyri',
                         'RfreesurferLabelToAimsTexture.GyriTexture')
    srNode.addDoubleLink(
        'RfreesurferResampleLabels.SulciGyri',
        'RfreesurferLabelToAimsTexture.SulciGyriTexture')

    # 12
    slNode.addChild('LfreesurferTexturesToGii',
                    ProcessExecutionNode('freesurferTexturesToGii',
                                         optional=1))
    eNode.addDoubleLink('lat1.left.LfreesurferTexturesToGii.Curv', 'leftCurv')
    eNode.addDoubleLink('lat1.left.LfreesurferTexturesToGii.Thickness',
                        'leftThickness')
    eNode.addDoubleLink('lat1.left.LfreesurferTexturesToGii.AvgCurv',
                        'leftAvgCurv')
    eNode.addDoubleLink('lat1.left.LfreesurferTexturesToGii.CurvPial',
                        'leftCurvPial')

    srNode.addChild('RfreesurferTexturesToGii',
                    ProcessExecutionNode('freesurferTexturesToGii',
                                         optional=1))
    eNode.addDoubleLink('lat1.right.RfreesurferTexturesToGii.Curv',
                        'rightCurv')
    eNode.addDoubleLink('lat1.right.RfreesurferTexturesToGii.Thickness',
                        'rightThickness')
    eNode.addDoubleLink('lat1.right.RfreesurferTexturesToGii.AvgCurv',
                        'rightAvgCurv')
    eNode.addDoubleLink('lat1.right.RfreesurferTexturesToGii.CurvPial',
                        'rightCurvPial')

    # 14
    slNode.addChild('LfreesurferResamplingDataTextures',
                    ProcessExecutionNode('freesurferResamplingDataTextures',
                                         optional=1))
    slNode.LfreesurferResamplingDataTextures.removeLink('Isin', 'OriginalMesh')
    slNode.LfreesurferResamplingDataTextures.removeLink('Curv', 'OriginalMesh')
    slNode.LfreesurferResamplingDataTextures.removeLink('AvgCurv',
                                                        'OriginalMesh')
    slNode.LfreesurferResamplingDataTextures.removeLink('CurvPial',
                                                        'OriginalMesh')
    slNode.LfreesurferResamplingDataTextures.removeLink('Thickness',
                                                        'OriginalMesh')
    slNode.addDoubleLink('LfreesurferResamplingDataTextures.OriginalMesh',
                         'LfreesurferMeshResampling.WhiteMesh')
    slNode.addDoubleLink('LfreesurferResamplingDataTextures.Isin',
                         'LfreesurferIsinComputing.Isin')
    slNode.addDoubleLink('LfreesurferResamplingDataTextures.Curv',
                         'LfreesurferTexturesToGii.GiftiCurv')
    slNode.addDoubleLink('LfreesurferResamplingDataTextures.AvgCurv',
                         'LfreesurferTexturesToGii.GiftiAvgCurv')
    slNode.addDoubleLink('LfreesurferResamplingDataTextures.CurvPial',
                         'LfreesurferTexturesToGii.GiftiCurvPial')
    slNode.addDoubleLink('LfreesurferResamplingDataTextures.Thickness',
                         'LfreesurferTexturesToGii.GiftiThickness')

    srNode.addChild('RfreesurferResamplingDataTextures',
                    ProcessExecutionNode('freesurferResamplingDataTextures',
                                         optional=1))
    srNode.RfreesurferResamplingDataTextures.removeLink('Isin', 'OriginalMesh')
    srNode.RfreesurferResamplingDataTextures.removeLink('Curv', 'OriginalMesh')
    srNode.RfreesurferResamplingDataTextures.removeLink('AvgCurv',
                                                        'OriginalMesh')
    srNode.RfreesurferResamplingDataTextures.removeLink('CurvPial',
                                                        'OriginalMesh')
    srNode.RfreesurferResamplingDataTextures.removeLink('Thickness',
                                                        'OriginalMesh')
    srNode.addDoubleLink('RfreesurferResamplingDataTextures.OriginalMesh',
                         'RfreesurferMeshResampling.WhiteMesh')
    srNode.addDoubleLink('RfreesurferResamplingDataTextures.Isin',
                         'RfreesurferIsinComputing.Isin')
    srNode.addDoubleLink('RfreesurferResamplingDataTextures.Curv',
                         'RfreesurferTexturesToGii.GiftiCurv')
    srNode.addDoubleLink('RfreesurferResamplingDataTextures.AvgCurv',
                         'RfreesurferTexturesToGii.GiftiAvgCurv')
    srNode.addDoubleLink('RfreesurferResamplingDataTextures.CurvPial',
                         'RfreesurferTexturesToGii.GiftiCurvPial')
    srNode.addDoubleLink('RfreesurferResamplingDataTextures.Thickness',
                         'RfreesurferTexturesToGii.GiftiThickness')

    # 15
    slNode.addChild('LfreesurferInflate',
                    ProcessExecutionNode('freesurferInflate',
                                         optional=1))
    slNode.addDoubleLink('LfreesurferInflate.White',
                         'LfreesurferMeshToAimsRef.AimsWhite')
    srNode.addChild('RfreesurferInflate',
                    ProcessExecutionNode('freesurferInflate',
                                         optional=1))
    srNode.addDoubleLink('RfreesurferInflate.White',
                         'RfreesurferMeshToAimsRef.AimsWhite')
    eNode.addDoubleLink('lat1.left.LfreesurferInflate.save_sequence',
                        'lat1.right.RfreesurferInflate.save_sequence')

    # 16
    qNode = ParallelExecutionNode('concat', optional=True, expandedInGui=True)
    eNode.addChild('concat', qNode)

    qNode.addChild('freesurferConcatenate',
                   ProcessExecutionNode('freesurferConcatenate',
                                        optional=1))
    qNode.freesurferConcatenate.removeLink('RightWhite', 'LeftWhite')
    qNode.freesurferConcatenate.removeLink('LeftPial', 'LeftWhite')
    qNode.freesurferConcatenate.removeLink('RightPial', 'LeftWhite')
    qNode.freesurferConcatenate.removeLink('LeftInflatedWhite', 'LeftWhite')
    qNode.freesurferConcatenate.removeLink('RightInflatedWhite', 'LeftWhite')
    qNode.freesurferConcatenate.removeLink('LeftInflatedWhite_sequence',
                                           'LeftInflatedWhite')
    qNode.freesurferConcatenate.removeLink('RightInflatedWhite_sequence',
                                           'RightInflatedWhite')
    eNode.addDoubleLink('concat.freesurferConcatenate.LeftWhite',
                        'lat1.left.LfreesurferMeshToAimsRef.AimsWhite')
    eNode.addDoubleLink('concat.freesurferConcatenate.RightWhite',
                        'lat1.right.RfreesurferMeshToAimsRef.AimsWhite')
    eNode.addDoubleLink('concat.freesurferConcatenate.LeftPial',
                        'lat1.left.LfreesurferMeshToAimsRef.AimsPial')
    eNode.addDoubleLink('concat.freesurferConcatenate.RightPial',
                        'lat1.right.RfreesurferMeshToAimsRef.AimsPial')
    eNode.addDoubleLink('concat.freesurferConcatenate.LeftInflatedWhite',
                        'lat1.left.LfreesurferInflate.InflatedWhite')
    eNode.addDoubleLink('concat.freesurferConcatenate.RightInflatedWhite',
                        'lat1.right.RfreesurferInflate.InflatedWhite')
    eNode.addDoubleLink(
        'concat.freesurferConcatenate.LeftInflatedWhite_sequence',
        'lat1.left.LfreesurferInflate.InflatedWhite_sequence')
    eNode.addDoubleLink(
        'concat.freesurferConcatenate.RightInflatedWhite_sequence',
        'lat1.right.RfreesurferInflate.InflatedWhite_sequence')

    # 17RfreesurferConversionMeshToGii
    qNode.addChild('freesurferConcatTex',
                   ProcessExecutionNode('freesurferConcatTex',
                                        optional=1))
    qNode.freesurferConcatTex.removeLink('RightGyri', 'LeftGyri')
    qNode.freesurferConcatTex.removeLink('LeftSulciGyri', 'LeftGyri')
    qNode.freesurferConcatTex.removeLink('RightSulciGyri', 'LeftGyri')
    eNode.addDoubleLink('concat.freesurferConcatTex.LeftGyri',
                        'lat1.left.LfreesurferResampleLabels.ResampledGyri')
    eNode.addDoubleLink('concat.freesurferConcatTex.RightGyri',
                        'lat1.right.RfreesurferResampleLabels.ResampledGyri')
    eNode.addDoubleLink(
        'concat.freesurferConcatTex.LeftSulciGyri',
        'lat1.left.LfreesurferResampleLabels.ResampledSulciGyri')
    eNode.addDoubleLink(
        'concat.freesurferConcatTex.RightSulciGyri',
        'lat1.right.RfreesurferResampleLabels.ResampledSulciGyri')

    # 18
    self.setExecutionNode(eNode)
