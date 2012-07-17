# -*- coding: utf-8 -*-
from brainvisa.processes import *

name = 'Brainvisa Freesurfer Pipeline'
userlevel = 2

signature = Signature(
  'anat', ReadDiskItem('FreesurferAnat', 'FreesurferMGZ'),

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
  self.linkParameters( 'leftPial', 'anat' )
  #self.linkParameters( 'leftWhite', 'anat' )
  #self.linkParameters( 'leftSphereReg', 'anat' )
  #self.linkParameters( 'leftThickness', 'anat' )
  self.linkParameters( 'leftCurv', 'anat' )
  #self.linkParameters( 'leftAvgCurv', 'anat' )
  #self.linkParameters( 'leftCurvPial', 'anat' )
  #self.linkParameters( 'leftGyri', 'anat' )
  #self.linkParameters( 'leftSulciGyri', 'anat' )

  self.linkParameters( 'rightPial', 'anat' )
  #self.linkParameters( 'rightWhite', 'anat' )
  #self.linkParameters( 'rightSphereReg', 'anat' )
  #self.linkParameters( 'rightThickness', 'anat' )
  self.linkParameters( 'rightCurv', 'anat' )
  #self.linkParameters( 'rightAvgCurv', 'anat' )
  #self.linkParameters( 'rightCurvPial', 'anat' )
  #self.linkParameters( 'rightGyri', 'anat' )
  #self.linkParameters( 'rightSulciGyri', 'anat' )

  #self.linkParameters( 'bv_anat', 'leftPial' )
  #self.linkParameters( 'bv_anat', 'rightPial' )

  eNode = SerialExecutionNode( self.name, parameterized=self )
  # 3b
  eNode.addChild('BfreesurferAnatToNii',
                 ProcessExecutionNode('freesurferAnatToNii',
                                      optional=1))
  eNode.addDoubleLink('BfreesurferAnatToNii.AnatImage', 'anat')
  
  
  # 4
  eNode.addChild('LfreesurferConversionMeshToGii',
                 ProcessExecutionNode('freesurferConversionMeshToGii',
                                      optional=1))
  
  #eNode.addDoubleLink('LfreesurferConversionMeshToGii.Pial', 'BfreesurferAnatToNii.AnatImage')
  
  #eNode.LfreesurferConversionMeshToGii.removeLink( 'White',
                                                   #'Pial' )
                                                    
  #eNode.LfreesurferConversionMeshToGii.removeLink( 'SphereReg',
                                                   #'Pial' )                                                  
                                     
  eNode.addDoubleLink('LfreesurferConversionMeshToGii.Pial', 'leftPial')
  eNode.addDoubleLink('LfreesurferConversionMeshToGii.White', 'leftWhite')
  eNode.addDoubleLink('LfreesurferConversionMeshToGii.SphereReg', 'leftSphereReg')
  eNode.addChild('RfreesurferConversionMeshToGii',
                 ProcessExecutionNode('freesurferConversionMeshToGii',
                                      optional=1))
                                      
  #eNode.RfreesurferConversionMeshToGii.removeLink( 'White',
                                                   #'Pial' )
                                                    
  #eNode.RfreesurferConversionMeshToGii.removeLink( 'SphereReg',
                                                   #'Pial' )   
                                      
  eNode.addDoubleLink('RfreesurferConversionMeshToGii.Pial', 'rightPial')
  eNode.addDoubleLink('RfreesurferConversionMeshToGii.White', 'rightWhite')
  eNode.addDoubleLink('RfreesurferConversionMeshToGii.SphereReg', 'rightSphereReg')
  # 5
  eNode.addChild('LfreesurferConversionGiiMeshToAims',
                ProcessExecutionNode('freesurferConversionGiiMeshToAims',
                                     optional=1))
  eNode.addDoubleLink('LfreesurferConversionGiiMeshToAims.PialGifti',
                'LfreesurferConversionMeshToGii.PialGifti')
  eNode.addChild('RfreesurferConversionGiiMeshToAims',
                ProcessExecutionNode('freesurferConversionGiiMeshToAims',
                                     optional=1))
  eNode.addDoubleLink('RfreesurferConversionGiiMeshToAims.PialGifti',
                'RfreesurferConversionMeshToGii.PialGifti')
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
  eNode.addDoubleLink('LfreesurferMeshResampling.PialMesh',
                'LfreesurferConversionGiiMeshToAims.PialMesh')
  eNode.addChild('RfreesurferMeshResampling',
                 ProcessExecutionNode('freesurferMeshResampling',
                                      optional=1))
  eNode.addDoubleLink('RfreesurferMeshResampling.PialMesh',
                'RfreesurferConversionGiiMeshToAims.PialMesh')
  # 8
  eNode.addChild('LfreesurferMeshToAimsRef',
                 ProcessExecutionNode('freesurferMeshToAimsRef',
                                      optional=1))
  eNode.addDoubleLink('LfreesurferMeshToAimsRef.ResampledPialMesh',
                'LfreesurferMeshResampling.ResampledPialMesh')
  eNode.addChild('RfreesurferMeshToAimsRef',
                 ProcessExecutionNode('freesurferMeshToAimsRef',
                                      optional=1))
  eNode.addDoubleLink('RfreesurferMeshToAimsRef.ResampledPialMesh',
                'RfreesurferMeshResampling.ResampledPialMesh')
  # 9
#  eNode.addChild('LfreesurferLabelAsciiConvert',
#                 ProcessExecutionNode('freesurferLabelAsciiConvert',
#                                      optional=1))
#  eNode.addDoubleLink('LfreesurferLabelAsciiConvert.Gyri', 'leftGyri')
#  eNode.addChild('RfreesurferLabelAsciiConvert',
#                 ProcessExecutionNode('freesurferLabelAsciiConvert',
#                                      optional=1))
#  eNode.addDoubleLink('RfreesurferLabelAsciiConvert.Gyri', 'rightGyri')
  # 10
#  eNode.addChild('LfreesurferLabelToTex',
#                 ProcessExecutionNode('freesurferLabelToTex',
#                                      optional=1))
#  eNode.addDoubleLink('LfreesurferLabelToTex.WhiteMesh',
#                'LfreesurferConversionGiiMeshToAims.WhiteMesh')
#  eNode.addChild('RfreesurferLabelToTex',
#                 ProcessExecutionNode('freesurferLabelToTex',
#                                      optional=1))
#  eNode.addDoubleLink('RfreesurferLabelToTex.WhiteMesh',
#                'RfreesurferConversionGiiMeshToAims.WhiteMesh')
  # 9/10
  eNode.addChild('LfreesurferLabelToAimsTexture',
                 ProcessExecutionNode('freesurferLabelToAimsTexture',
                                     optional=1))
                                     
  #eNode.LfreesurferLabelToAimsTexture.removeLink( 'Gyri',
                                                  #'WhiteMesh' )
                                                  
  #eNode.LfreesurferLabelToAimsTexture.removeLink( 'SulciGyri',
                                                  #'WhiteMesh' )                                                
                                     
  eNode.addDoubleLink('LfreesurferLabelToAimsTexture.WhiteMesh',
                      'LfreesurferConversionGiiMeshToAims.WhiteMesh')
  eNode.addDoubleLink('LfreesurferLabelToAimsTexture.Gyri', 'leftGyri')
  eNode.addDoubleLink('LfreesurferLabelToAimsTexture.SulciGyri', 'leftSulciGyri')
  eNode.addChild('RfreesurferLabelToAimsTexture',
                 ProcessExecutionNode('freesurferLabelToAimsTexture',
                                     optional=1))
                                     
  #eNode.RfreesurferLabelToAimsTexture.removeLink( 'Gyri',
                                                  #'WhiteMesh' )
                                                  
  #eNode.RfreesurferLabelToAimsTexture.removeLink( 'SulciGyri',
                                                  #'WhiteMesh' )                                   
                                     
  eNode.addDoubleLink('RfreesurferLabelToAimsTexture.WhiteMesh',
                      'RfreesurferConversionGiiMeshToAims.WhiteMesh')
  eNode.addDoubleLink('RfreesurferLabelToAimsTexture.Gyri', 'rightGyri')
  eNode.addDoubleLink('RfreesurferLabelToAimsTexture.SulciGyri', 'rightSulciGyri')
  # 11
  eNode.addChild('LfreesurferResampleLabels',
                 ProcessExecutionNode('freesurferResampleLabels',
                                     optional=1))
  eNode.addDoubleLink('LfreesurferResampleLabels.WhiteMesh',
                'LfreesurferConversionGiiMeshToAims.WhiteMesh')
  eNode.addChild('RfreesurferResampleLabels',
                 ProcessExecutionNode('freesurferResampleLabels',
                                     optional=1))
  eNode.addDoubleLink('RfreesurferResampleLabels.WhiteMesh',
                'RfreesurferConversionGiiMeshToAims.WhiteMesh')
  # 12
  eNode.addChild('LfreesurferTexturesToGii',
                 ProcessExecutionNode('freesurferTexturesToGii',
                                      optional=1))
                                      
  #eNode.LfreesurferTexturesToGii.removeLink( 'AvgCurv',
                                             #'Curv' )
                                             
  #eNode.LfreesurferTexturesToGii.removeLink( 'CurvPial',
                                             #'Curv' )
                                             
  #eNode.LfreesurferTexturesToGii.removeLink( 'Thickness',
                                             #'Curv' )                                           
                                      
  eNode.addDoubleLink('LfreesurferTexturesToGii.Curv', 'leftCurv')
  eNode.addDoubleLink('LfreesurferTexturesToGii.Thickness', 'leftThickness')
  eNode.addDoubleLink('LfreesurferTexturesToGii.AvgCurv', 'leftAvgCurv')
  eNode.addDoubleLink('LfreesurferTexturesToGii.CurvPial', 'leftCurvPial')
  eNode.addChild('RfreesurferTexturesToGii',
                 ProcessExecutionNode('freesurferTexturesToGii',
                                      optional=1))
                                      
  #eNode.RfreesurferTexturesToGii.removeLink( 'AvgCurv',
                                             #'Curv' )
                                             
  #eNode.RfreesurferTexturesToGii.removeLink( 'CurvPial',
                                             #'Curv' )
                                             
  #eNode.RfreesurferTexturesToGii.removeLink( 'Thickness',
                                             #'Curv' )                                      
                                      
  eNode.addDoubleLink('RfreesurferTexturesToGii.Curv', 'rightCurv')
  eNode.addDoubleLink('RfreesurferTexturesToGii.Thickness', 'rightThickness')
  eNode.addDoubleLink('RfreesurferTexturesToGii.AvgCurv', 'rightAvgCurv')
  eNode.addDoubleLink('RfreesurferTexturesToGii.CurvPial', 'rightCurvPial')
  # 13
  eNode.addChild('LfreesurferGiiTexturesToAims',
                 ProcessExecutionNode('freesurferGiiTexturesToAims',
                                      optional=1))
  eNode.addDoubleLink('LfreesurferGiiTexturesToAims.GiftiCurv',
                'LfreesurferTexturesToGii.GiftiCurv')
  eNode.addChild('RfreesurferGiiTexturesToAims',
                 ProcessExecutionNode('freesurferGiiTexturesToAims',
                                      optional=1))
  eNode.addDoubleLink('RfreesurferGiiTexturesToAims.GiftiCurv',
                'RfreesurferTexturesToGii.GiftiCurv')
  # 14
  eNode.addChild('LfreesurferResamplingDataTextures',
                 ProcessExecutionNode('freesurferResamplingDataTextures',
                                      optional=1))
  eNode.addDoubleLink('LfreesurferResamplingDataTextures.OriginalMesh',
                'LfreesurferMeshToAimsRef.AimsWhite')
  eNode.addChild('RfreesurferResamplingDataTextures',
                 ProcessExecutionNode('freesurferResamplingDataTextures',
                                      optional=1))
  eNode.addDoubleLink('RfreesurferResamplingDataTextures.OriginalMesh',
                'RfreesurferMeshToAimsRef.AimsWhite')
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
  eNode.addDoubleLink('freesurferConcatenate.LeftWhite',
                'LfreesurferMeshToAimsRef.AimsWhite')
  # 17
  eNode.addChild('freesurferConcatTex',
                 ProcessExecutionNode('freesurferConcatTex',
                                      optional=1))
  eNode.addDoubleLink('freesurferConcatTex.LeftGyri',
                'LfreesurferResampleLabels.ResampledGyri')
  # 18
  self.setExecutionNode( eNode )


