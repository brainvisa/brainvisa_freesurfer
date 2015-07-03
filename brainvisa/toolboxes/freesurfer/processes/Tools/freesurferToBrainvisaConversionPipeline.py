# -*- coding: utf-8 -*-
from brainvisa.processes import *

name = 'Freesurfer outputs To BrainVisa conversion pipeline'
userLevel = 1

signature = Signature(
    'anat', ReadDiskItem('RawFreesurferAnat', 'FreesurferMGZ',
        enableConversion=False),
    'nu', ReadDiskItem('Nu FreesurferAnat', 'FreesurferMGZ',
        enableConversion=False),
    'ribbon', ReadDiskItem('Ribbon Freesurfer', 'FreesurferMGZ',
        enableConversion=False),

    'leftPial', ReadDiskItem('FreesurferType', 'FreesurferPial',
            requiredAttributes = {'side': 'left'}),
    'leftWhite', ReadDiskItem('FreesurferType', 'FreesurferWhite',
            requiredAttributes = {'side': 'left'}),
    'leftSphereReg', ReadDiskItem('FreesurferType', 'FreesurferSphereReg',
            requiredAttributes = {'side': 'left'}),
    'leftThickness', ReadDiskItem('FreesurferType', 'FreesurferThickness',
            requiredAttributes = {'side': 'left'}),
    'leftCurv', ReadDiskItem('FreesurferType', 'FreesurferCurv',
            requiredAttributes = {'side': 'left'}),
    'leftAvgCurv', ReadDiskItem('FreesurferType', 'FreesurferAvgCurv',
            requiredAttributes = {'side': 'left'}),
    'leftCurvPial', ReadDiskItem('FreesurferType', 'FreesurferCurvPial',
            requiredAttributes = {'side': 'left'}),
    'leftGyri', ReadDiskItem('FreesurferGyriTexture', 'FreesurferParcellation',
            requiredAttributes = {'side': 'left'}),
    'leftSulciGyri',
            ReadDiskItem('FreesurferSulciGyriTexture', 'FreesurferParcellation',
            requiredAttributes = {'side': 'left'}),
    
    'rightPial', ReadDiskItem('FreesurferType', 'FreesurferPial',
            requiredAttributes = {'side': 'right'}),
    'rightWhite', ReadDiskItem('FreesurferType', 'FreesurferWhite',
            requiredAttributes = {'side': 'right'}),
    'rightSphereReg', ReadDiskItem('FreesurferType', 'FreesurferSphereReg',
            requiredAttributes = {'side': 'right'}),
    'rightThickness', ReadDiskItem('FreesurferType', 'FreesurferThickness',
            requiredAttributes = {'side': 'right'}),
    'rightCurv', ReadDiskItem('FreesurferType', 'FreesurferCurv',
            requiredAttributes = {'side': 'right'}),
    'rightAvgCurv', ReadDiskItem('FreesurferType', 'FreesurferAvgCurv',
            requiredAttributes = {'side': 'right'}),
    'rightCurvPial', ReadDiskItem('FreesurferType', 'FreesurferCurvPial',
            requiredAttributes = {'side': 'right'}),
    'rightGyri', ReadDiskItem('FreesurferGyriTexture', 'FreesurferParcellation',
            requiredAttributes = {'side': 'right'}),
    'rightSulciGyri',
            ReadDiskItem('FreesurferSulciGyriTexture', 'FreesurferParcellation',
            requiredAttributes = {'side': 'right'}),
  
  #'bv_anat', ReadDiskItem('Raw T1 MRI', 'NIFTI-1 image')
    )

def initialization( self ):
    self.linkParameters('nu', 'anat')
    self.linkParameters('ribbon', 'anat')
    
    self.linkParameters('leftPial', 'anat')
    self.linkParameters('leftCurv', 'anat')

    self.linkParameters('rightPial', 'anat')
    self.linkParameters('rightCurv', 'anat')

    eNode = SerialExecutionNode(self.name, parameterized=self)

    eNode.addChild('CreateReferential',
                   ProcessExecutionNode('newreferential', optional=1))
    eNode.addDoubleLink('CreateReferential.data', 'anat')

    # 3b
    eNode.addChild('BfreesurferImageToNii',
                    ProcessExecutionNode('freesurferAnatToNii', optional=1))
    eNode.BfreesurferImageToNii.removeLink('NuImage', 'AnatImage')
    eNode.BfreesurferImageToNii.removeLink('RibbonImage', 'AnatImage')
    eNode.BfreesurferImageToNii.removeLink('referential', 'AnatImage')
    
    eNode.addDoubleLink('BfreesurferImageToNii.AnatImage', 'anat')
    eNode.addDoubleLink('BfreesurferImageToNii.NuImage', 'nu')
    eNode.addDoubleLink('BfreesurferImageToNii.RibbonImage', 'ribbon')
    eNode.addDoubleLink('BfreesurferImageToNii.referential',
                        'CreateReferential.referential')

    # referential
    eNode.addChild('CreateReferentials',
                   ProcessExecutionNode('AddScannerBasedReferential', optional=1))
    eNode.CreateReferentials.removeLink('referential_volume_input', 'volume_input')
    eNode.addDoubleLink('CreateReferentials.volume_input',
                        'BfreesurferImageToNii.NiiAnatImage')
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
                        'BfreesurferImageToNii.NiiAnatImage')


    eNode.addChild('CreateMeshesTransformation',
                   ProcessExecutionNode('freesurferAnatToMeshesTransformation',
                                        optional=1))
    eNode.CreateMeshesTransformation.removeLink('freesurfer_meshes_referential',
                                                'anat')
    eNode.CreateMeshesTransformation.removeLink('anat_referential', 'anat')
    eNode.addDoubleLink('BfreesurferImageToNii.NiiAnatImage',
                        'CreateMeshesTransformation.anat')
    eNode.addDoubleLink('CreateMeshesReferential.meshes_referential',
                        'CreateMeshesTransformation.freesurfer_meshes_referential')
    eNode.addDoubleLink('CreateReferential.referential',
                        'CreateMeshesTransformation.anat_referential')

    # 4 - Left
    eNode.addChild('LfreesurferConversionMeshToGii',
                   ProcessExecutionNode('freesurferConversionMeshToGii',
                                        optional=1))
    #eNode.LfreesurferConversionMeshToGii.removeLink('White', 'Pial')
    #eNode.LfreesurferConversionMeshToGii.removeLink('SphereReg', 'Pial')
    eNode.LfreesurferConversionMeshToGii.removeLink('meshes_referential',
                                                    'PialGifti')

    eNode.addDoubleLink('LfreesurferConversionMeshToGii.Pial', 'leftPial')
    eNode.addDoubleLink('LfreesurferConversionMeshToGii.White', 'leftWhite')
    eNode.addDoubleLink('LfreesurferConversionMeshToGii.SphereReg', 'leftSphereReg')
    eNode.addDoubleLink('LfreesurferConversionMeshToGii.meshes_referential',
                        'CreateMeshesReferential.meshes_referential')

    #4  -Right
    eNode.addChild('RfreesurferConversionMeshToGii',
                   ProcessExecutionNode('freesurferConversionMeshToGii',
                                        optional=1))
    #eNode.RfreesurferConversionMeshToGii.removeLink('White', 'Pial')
    #eNode.RfreesurferConversionMeshToGii.removeLink('SphereReg', 'Pial')
    eNode.RfreesurferConversionMeshToGii.removeLink('meshes_referential',
                                                    'PialGifti')

    eNode.addDoubleLink('RfreesurferConversionMeshToGii.Pial', 'rightPial')
    eNode.addDoubleLink('RfreesurferConversionMeshToGii.White', 'rightWhite')
    eNode.addDoubleLink('RfreesurferConversionMeshToGii.SphereReg', 'rightSphereReg')
    eNode.addDoubleLink('RfreesurferConversionMeshToGii.meshes_referential',
                        'CreateMeshesReferential.meshes_referential')

    # 6
    eNode.addChild('LfreesurferIsinComputing',
                   ProcessExecutionNode('freesurferIsinComputing',
                                        optional=1))
    eNode.addDoubleLink('LfreesurferIsinComputing.SphereRegMesh',
                        'LfreesurferConversionMeshToGii.SphereRegGifti')
    eNode.addChild('RfreesurferIsinComputing',
                   ProcessExecutionNode('freesurferIsinComputing',
                                        optional=1))
    eNode.addDoubleLink('RfreesurferIsinComputing.SphereRegMesh',
                        'RfreesurferConversionMeshToGii.SphereRegGifti')
    
    # 7
    eNode.addChild('LfreesurferMeshResampling',
                   ProcessExecutionNode('freesurferMeshResampling',
                                        optional=1))
    eNode.LfreesurferMeshResampling.removeLink('WhiteMesh', 'PialMesh')
    eNode.LfreesurferMeshResampling.removeLink('Isin', 'PialMesh')
    eNode.LfreesurferMeshResampling.removeLink('destination', 'PialMesh')
    eNode.addDoubleLink('LfreesurferMeshResampling.PialMesh',
                        'LfreesurferConversionMeshToGii.PialGifti')
    eNode.addDoubleLink('LfreesurferMeshResampling.WhiteMesh',
                        'LfreesurferConversionMeshToGii.WhiteGifti')
    eNode.addDoubleLink('LfreesurferMeshResampling.destination',
                        'LfreesurferIsinComputing.destination')
    eNode.addDoubleLink('LfreesurferMeshResampling.Isin',
                        'LfreesurferIsinComputing.Isin')

    eNode.addChild('RfreesurferMeshResampling',
                   ProcessExecutionNode('freesurferMeshResampling',
                                        optional=1))
    eNode.RfreesurferMeshResampling.removeLink('WhiteMesh', 'PialMesh')
    eNode.RfreesurferMeshResampling.removeLink('Isin', 'PialMesh')
    eNode.RfreesurferMeshResampling.removeLink('destination', 'PialMesh')
    eNode.addDoubleLink('RfreesurferMeshResampling.PialMesh',
                        'RfreesurferConversionMeshToGii.PialGifti')
    eNode.addDoubleLink('RfreesurferMeshResampling.WhiteMesh',
                        'RfreesurferConversionMeshToGii.WhiteGifti')
    eNode.addDoubleLink('RfreesurferMeshResampling.destination',
                        'RfreesurferIsinComputing.destination')
    eNode.addDoubleLink('RfreesurferMeshResampling.Isin',
                        'RfreesurferIsinComputing.Isin')
    # 8
    eNode.addChild('LfreesurferMeshToAimsRef',
                   ProcessExecutionNode('freesurferMeshToAimsRef',
                                        optional=1))
    eNode.LfreesurferMeshToAimsRef.removeLink('ResampledWhiteMesh',
                                              'ResampledPialMesh' )
    eNode.LfreesurferMeshToAimsRef.removeLink('bv_anat', 'ResampledPialMesh')
    eNode.addDoubleLink('LfreesurferMeshToAimsRef.ResampledPialMesh',
                        'LfreesurferMeshResampling.ResampledPialMesh')
    eNode.addDoubleLink('LfreesurferMeshToAimsRef.ResampledWhiteMesh',
                        'LfreesurferMeshResampling.ResampledWhiteMesh')
    eNode.addDoubleLink('LfreesurferMeshToAimsRef.bv_anat',
                        'BfreesurferImageToNii.NiiAnatImage')

    eNode.addChild('RfreesurferMeshToAimsRef',
                   ProcessExecutionNode('freesurferMeshToAimsRef',
                                        optional=1))
    eNode.RfreesurferMeshToAimsRef.removeLink('bv_anat', 'ResampledPialMesh')
    eNode.addDoubleLink('RfreesurferMeshToAimsRef.ResampledPialMesh',
                        'RfreesurferMeshResampling.ResampledPialMesh')
    eNode.addDoubleLink('RfreesurferMeshToAimsRef.ResampledWhiteMesh',
                        'RfreesurferMeshResampling.ResampledWhiteMesh')
    eNode.addDoubleLink('RfreesurferMeshToAimsRef.bv_anat',
                        'BfreesurferImageToNii.NiiAnatImage')

    # 9/10
    eNode.addChild('LfreesurferLabelToAimsTexture',
                   ProcessExecutionNode('freesurferLabelToAimsTexture',
                                        optional=1))
    eNode.addDoubleLink('LfreesurferLabelToAimsTexture.WhiteMesh',
                        'LfreesurferConversionMeshToGii.WhiteGifti')
    eNode.addDoubleLink('LfreesurferLabelToAimsTexture.Gyri', 'leftGyri')
    eNode.addDoubleLink('LfreesurferLabelToAimsTexture.SulciGyri',
                        'leftSulciGyri')

    eNode.addChild('RfreesurferLabelToAimsTexture',
                   ProcessExecutionNode('freesurferLabelToAimsTexture',
                                        optional=1))
    eNode.addDoubleLink('RfreesurferLabelToAimsTexture.WhiteMesh',
                        'RfreesurferConversionMeshToGii.WhiteGifti')
    eNode.addDoubleLink('RfreesurferLabelToAimsTexture.Gyri', 'rightGyri')
    eNode.addDoubleLink('RfreesurferLabelToAimsTexture.SulciGyri',
                        'rightSulciGyri')
    # 11
    eNode.addChild('LfreesurferResampleLabels',
                   ProcessExecutionNode('freesurferResampleLabels',
                                        optional=1))
    eNode.LfreesurferResampleLabels.removeLink('Isin', 'WhiteMesh')
    eNode.LfreesurferResampleLabels.removeLink('Gyri', 'WhiteMesh')
    eNode.LfreesurferResampleLabels.removeLink('SulciGyri', 'WhiteMesh')
    eNode.addDoubleLink('LfreesurferResampleLabels.WhiteMesh',
                        'LfreesurferConversionMeshToGii.WhiteGifti')
    eNode.addDoubleLink('LfreesurferResampleLabels.Isin',
                        'LfreesurferIsinComputing.Isin')
    eNode.addDoubleLink('LfreesurferResampleLabels.Gyri',
                        'LfreesurferLabelToAimsTexture.GyriTexture')
    eNode.addDoubleLink('LfreesurferResampleLabels.SulciGyri',
                        'LfreesurferLabelToAimsTexture.SulciGyriTexture')

    eNode.addChild('RfreesurferResampleLabels',
                   ProcessExecutionNode('freesurferResampleLabels',
                                        optional=1))
    eNode.RfreesurferResampleLabels.removeLink('Isin', 'WhiteMesh')
    eNode.RfreesurferResampleLabels.removeLink('Gyri', 'WhiteMesh')
    eNode.RfreesurferResampleLabels.removeLink('SulciGyri', 'WhiteMesh')
    eNode.addDoubleLink('RfreesurferResampleLabels.WhiteMesh',
                        'RfreesurferConversionMeshToGii.WhiteGifti')
    eNode.addDoubleLink('RfreesurferResampleLabels.Isin',
                        'RfreesurferIsinComputing.Isin')
    eNode.addDoubleLink('RfreesurferResampleLabels.Gyri',
                        'RfreesurferLabelToAimsTexture.GyriTexture')
    eNode.addDoubleLink('RfreesurferResampleLabels.SulciGyri',
                        'RfreesurferLabelToAimsTexture.SulciGyriTexture')

    # 12
    eNode.addChild('LfreesurferTexturesToGii',
                   ProcessExecutionNode('freesurferTexturesToGii',
                                        optional=1))
    eNode.addDoubleLink('LfreesurferTexturesToGii.Curv', 'leftCurv')
    eNode.addDoubleLink('LfreesurferTexturesToGii.Thickness', 'leftThickness')
    eNode.addDoubleLink('LfreesurferTexturesToGii.AvgCurv', 'leftAvgCurv')
    eNode.addDoubleLink('LfreesurferTexturesToGii.CurvPial', 'leftCurvPial')

    eNode.addChild('RfreesurferTexturesToGii',
                   ProcessExecutionNode('freesurferTexturesToGii',
                                        optional=1))
    eNode.addDoubleLink('RfreesurferTexturesToGii.Curv', 'rightCurv')
    eNode.addDoubleLink('RfreesurferTexturesToGii.Thickness', 'rightThickness')
    eNode.addDoubleLink('RfreesurferTexturesToGii.AvgCurv', 'rightAvgCurv')
    eNode.addDoubleLink('RfreesurferTexturesToGii.CurvPial', 'rightCurvPial')

    # 14
    eNode.addChild('LfreesurferResamplingDataTextures',
                   ProcessExecutionNode('freesurferResamplingDataTextures',
                                        optional=1))
    eNode.LfreesurferResamplingDataTextures.removeLink('Isin', 'OriginalMesh')
    eNode.LfreesurferResamplingDataTextures.removeLink('Curv', 'OriginalMesh')
    eNode.LfreesurferResamplingDataTextures.removeLink('AvgCurv',
                                                       'OriginalMesh')
    eNode.LfreesurferResamplingDataTextures.removeLink('CurvPial',
                                                       'OriginalMesh')
    eNode.LfreesurferResamplingDataTextures.removeLink('Thickness',
                                                       'OriginalMesh')
    eNode.addDoubleLink('LfreesurferResamplingDataTextures.OriginalMesh',
                        'LfreesurferMeshResampling.WhiteMesh')
    eNode.addDoubleLink('LfreesurferResamplingDataTextures.Isin',
                        'LfreesurferIsinComputing.Isin')
    eNode.addDoubleLink('LfreesurferResamplingDataTextures.Curv',
                        'LfreesurferTexturesToGii.GiftiCurv')
    eNode.addDoubleLink('LfreesurferResamplingDataTextures.AvgCurv',
                        'LfreesurferTexturesToGii.GiftiAvgCurv')
    eNode.addDoubleLink('LfreesurferResamplingDataTextures.CurvPial',
                        'LfreesurferTexturesToGii.GiftiCurvPial')
    eNode.addDoubleLink('LfreesurferResamplingDataTextures.Thickness',
                        'LfreesurferTexturesToGii.GiftiThickness')

    eNode.addChild('RfreesurferResamplingDataTextures',
                   ProcessExecutionNode('freesurferResamplingDataTextures',
                                        optional=1))
    eNode.RfreesurferResamplingDataTextures.removeLink('Isin', 'OriginalMesh')
    eNode.RfreesurferResamplingDataTextures.removeLink('Curv', 'OriginalMesh')
    eNode.RfreesurferResamplingDataTextures.removeLink('AvgCurv',
                                                       'OriginalMesh')
    eNode.RfreesurferResamplingDataTextures.removeLink('CurvPial',
                                                       'OriginalMesh')
    eNode.RfreesurferResamplingDataTextures.removeLink('Thickness',
                                                       'OriginalMesh')
    eNode.addDoubleLink('RfreesurferResamplingDataTextures.OriginalMesh',
                        'RfreesurferMeshResampling.WhiteMesh')
    eNode.addDoubleLink('RfreesurferResamplingDataTextures.Isin',
                        'RfreesurferIsinComputing.Isin')
    eNode.addDoubleLink('RfreesurferResamplingDataTextures.Curv',
                        'RfreesurferTexturesToGii.GiftiCurv')
    eNode.addDoubleLink('RfreesurferResamplingDataTextures.AvgCurv',
                        'RfreesurferTexturesToGii.GiftiAvgCurv')
    eNode.addDoubleLink('RfreesurferResamplingDataTextures.CurvPial',
                        'RfreesurferTexturesToGii.GiftiCurvPial')
    eNode.addDoubleLink('RfreesurferResamplingDataTextures.Thickness',
                        'RfreesurferTexturesToGii.GiftiThickness')

    # 15
    eNode.addChild('LfreesurferInflate',
                   ProcessExecutionNode('freesurferInflate',
                                        optional=1))
    eNode.addDoubleLink('LfreesurferInflate.White',
                        'LfreesurferMeshToAimsRef.AimsWhite')
    eNode.addChild('RfreesurferInflate',
                   ProcessExecutionNode('freesurferInflate',
                                        optional=1))
    eNode.addDoubleLink('RfreesurferInflate.White',
                        'RfreesurferMeshToAimsRef.AimsWhite')

    # 16
    eNode.addChild('freesurferConcatenate',
                   ProcessExecutionNode('freesurferConcatenate',
                                        optional=1))
    eNode.freesurferConcatenate.removeLink('RightWhite', 'LeftWhite')
    eNode.freesurferConcatenate.removeLink('LeftPial', 'LeftWhite')
    eNode.freesurferConcatenate.removeLink('RightPial', 'LeftWhite')
    eNode.freesurferConcatenate.removeLink('LeftInflatedWhite', 'LeftWhite')
    eNode.freesurferConcatenate.removeLink('RightInflatedWhite', 'LeftWhite')
    eNode.addDoubleLink('freesurferConcatenate.LeftWhite',
                        'LfreesurferMeshToAimsRef.AimsWhite')
    eNode.addDoubleLink('freesurferConcatenate.RightWhite',
                        'RfreesurferMeshToAimsRef.AimsWhite')
    eNode.addDoubleLink('freesurferConcatenate.LeftPial',
                        'LfreesurferMeshToAimsRef.AimsPial')
    eNode.addDoubleLink('freesurferConcatenate.RightPial',
                        'RfreesurferMeshToAimsRef.AimsPial')
    eNode.addDoubleLink('freesurferConcatenate.LeftInflatedWhite',
                        'LfreesurferInflate.InflatedWhite')
    eNode.addDoubleLink('freesurferConcatenate.RightInflatedWhite',
                        'RfreesurferInflate.InflatedWhite')

    # 17
    eNode.addChild('freesurferConcatTex',
                   ProcessExecutionNode('freesurferConcatTex',
                                        optional=1))
    eNode.freesurferConcatTex.removeLink('RightGyri', 'LeftGyri')
    eNode.freesurferConcatTex.removeLink('LeftSulciGyri', 'LeftGyri')
    eNode.freesurferConcatTex.removeLink('RightSulciGyri', 'LeftGyri')
    eNode.addDoubleLink('freesurferConcatTex.LeftGyri',
                        'LfreesurferResampleLabels.ResampledGyri')
    eNode.addDoubleLink('freesurferConcatTex.RightGyri',
                        'RfreesurferResampleLabels.ResampledGyri')
    eNode.addDoubleLink('freesurferConcatTex.LeftSulciGyri',
                        'LfreesurferResampleLabels.ResampledSulciGyri')
    eNode.addDoubleLink('freesurferConcatTex.RightSulciGyri',
                        'RfreesurferResampleLabels.ResampledSulciGyri')

    # 18
    self.setExecutionNode( eNode )


