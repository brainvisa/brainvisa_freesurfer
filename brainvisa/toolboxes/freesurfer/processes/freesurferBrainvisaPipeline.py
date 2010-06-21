from neuroProcesses import *

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
  self.linkParameters( 'leftWhite', 'anat' )
  self.linkParameters( 'leftSphereReg', 'anat' )
  self.linkParameters( 'leftThickness', 'anat' )
  self.linkParameters( 'leftCurv', 'anat' )
  self.linkParameters( 'leftAvgCurv', 'anat' )
  self.linkParameters( 'leftCurvPial', 'anat' )
  self.linkParameters( 'leftGyri', 'anat' )
  self.linkParameters( 'leftSulciGyri', 'anat' )

  self.linkParameters( 'rightPial', 'anat' )
  self.linkParameters( 'rightWhite', 'anat' )
  self.linkParameters( 'rightSphereReg', 'anat' )
  self.linkParameters( 'rightThickness', 'anat' )
  self.linkParameters( 'rightCurv', 'anat' )
  self.linkParameters( 'rightAvgCurv', 'anat' )
  self.linkParameters( 'rightCurvPial', 'anat' )
  self.linkParameters( 'rightGyri', 'anat' )
  self.linkParameters( 'rightSulciGyri', 'anat' )

  #self.linkParameters( 'bv_anat', 'leftPial' )
  #self.linkParameters( 'bv_anat', 'rightPial' )

  eNode = SerialExecutionNode( self.name, parameterized=self )
  # 3b
  eNode.addChild('BfreesurferAnatToNii',
                 ProcessExecutionNode('freesurferAnatToNii',
                                      optional=1))
  eNode.addLink('BfreesurferAnatToNii.AnatImage', 'anat')
  # 4
  eNode.addChild('LfreesurferConversionMeshToGii',
                 ProcessExecutionNode('freesurferConversionMeshToGii',
                                      optional=1))
  eNode.addLink('LfreesurferConversionMeshToGii.Pial', 'leftPial')
  eNode.addChild('RfreesurferConversionMeshToGii',
                 ProcessExecutionNode('freesurferConversionMeshToGii',
                                      optional=1))
  eNode.addLink('RfreesurferConversionMeshToGii.Pial', 'rightPial')
  # 5
  eNode.addChild('LfreesurferConversionGiiMeshToAims',
                ProcessExecutionNode('freesurferConversionGiiMeshToAims',
                                     optional=1))
  eNode.addLink('LfreesurferConversionGiiMeshToAims.PialGifti',
                'LfreesurferConversionMeshToGii.PialGifti')
  eNode.addChild('RfreesurferConversionGiiMeshToAims',
                ProcessExecutionNode('freesurferConversionGiiMeshToAims',
                                     optional=1))
  eNode.addLink('RfreesurferConversionGiiMeshToAims.PialGifti',
                'RfreesurferConversionMeshToGii.PialGifti')
  # 6
  eNode.addChild('LfreesurferIsinComputing',
                 ProcessExecutionNode('freesurferIsinComputing',
                                      optional=1))
  eNode.addLink('LfreesurferIsinComputing.SphereRegMesh',
                 'LfreesurferConversionMeshToGii.SphereRegGifti')
  eNode.addChild('RfreesurferIsinComputing',
                 ProcessExecutionNode('freesurferIsinComputing',
                                      optional=1))
  eNode.addLink('RfreesurferIsinComputing.SphereRegMesh',
                 'RfreesurferConversionMeshToGii.SphereRegGifti')
  # 7
  eNode.addChild('LfreesurferMeshResampling',
                 ProcessExecutionNode('freesurferMeshResampling',
                                      optional=1))
  eNode.addLink('LfreesurferMeshResampling.PialMesh',
                'LfreesurferConversionGiiMeshToAims.PialMesh')
  eNode.addChild('RfreesurferMeshResampling',
                 ProcessExecutionNode('freesurferMeshResampling',
                                      optional=1))
  eNode.addLink('RfreesurferMeshResampling.PialMesh',
                'RfreesurferConversionGiiMeshToAims.PialMesh')
  # 8
  eNode.addChild('LfreesurferMessToAimsRef',
                 ProcessExecutionNode('freesurferMessToAimsRef',
                                      optional=1))
  eNode.addLink('LfreesurferMessToAimsRef.ResampledPialMesh',
                'LfreesurferMeshResampling.ResampledPialMesh')
  eNode.addChild('RfreesurferMessToAimsRef',
                 ProcessExecutionNode('freesurferMessToAimsRef',
                                      optional=1))
  eNode.addLink('RfreesurferMessToAimsRef.ResampledPialMesh',
                'RfreesurferMeshResampling.ResampledPialMesh')
  # 9
#  eNode.addChild('LfreesurferLabelAsciiConvert',
#                 ProcessExecutionNode('freesurferLabelAsciiConvert',
#                                      optional=1))
#  eNode.addLink('LfreesurferLabelAsciiConvert.Gyri', 'leftGyri')
#  eNode.addChild('RfreesurferLabelAsciiConvert',
#                 ProcessExecutionNode('freesurferLabelAsciiConvert',
#                                      optional=1))
#  eNode.addLink('RfreesurferLabelAsciiConvert.Gyri', 'rightGyri')
  # 10
#  eNode.addChild('LfreesurferLabelToTex',
#                 ProcessExecutionNode('freesurferLabelToTex',
#                                      optional=1))
#  eNode.addLink('LfreesurferLabelToTex.WhiteMesh',
#                'LfreesurferConversionGiiMeshToAims.WhiteMesh')
#  eNode.addChild('RfreesurferLabelToTex',
#                 ProcessExecutionNode('freesurferLabelToTex',
#                                      optional=1))
#  eNode.addLink('RfreesurferLabelToTex.WhiteMesh',
#                'RfreesurferConversionGiiMeshToAims.WhiteMesh')
  # 9/10
  eNode.addChild('LfreesurferLabelToAimsTexture',
                 ProcessExecutionNode('freesurferLabelToAimsTexture',
                                     optional=1))
  eNode.addLink('LfreesurferLabelToAimsTexture.WhiteMesh',
                'LfreesurferConversionGiiMeshToAims.WhiteMesh')
  eNode.addChild('RfreesurferLabelToAimsTexture',
                 ProcessExecutionNode('freesurferLabelToAimsTexture',
                                     optional=1))
  eNode.addLink('RfreesurferLabelToAimsTexture.WhiteMesh',
                'RfreesurferConversionGiiMeshToAims.WhiteMesh')
  # 11
  eNode.addChild('LfreesurferResampleLabels',
                 ProcessExecutionNode('freesurferResampleLabels',
                                     optional=1))
  eNode.addLink('LfreesurferResampleLabels.WhiteMesh',
                'LfreesurferConversionGiiMeshToAims.WhiteMesh')
  eNode.addChild('RfreesurferResampleLabels',
                 ProcessExecutionNode('freesurferResampleLabels',
                                     optional=1))
  eNode.addLink('RfreesurferResampleLabels.WhiteMesh',
                'RfreesurferConversionGiiMeshToAims.WhiteMesh')
  # 12
  eNode.addChild('LfreesurferTexturesToGii',
                 ProcessExecutionNode('freesurferTexturesToGii',
                                      optional=1))
  eNode.addLink('LfreesurferTexturesToGii.Curv', 'leftCurv')
  eNode.addChild('RfreesurferTexturesToGii',
                 ProcessExecutionNode('freesurferTexturesToGii',
                                      optional=1))
  eNode.addLink('RfreesurferTexturesToGii.Curv', 'rightCurv')
  # 13
  eNode.addChild('LfreesurferGiiTexturesToAims',
                 ProcessExecutionNode('freesurferGiiTexturesToAims',
                                      optional=1))
  eNode.addLink('LfreesurferGiiTexturesToAims.GiftiCurv',
                'LfreesurferTexturesToGii.GiftiCurv')
  eNode.addChild('RfreesurferGiiTexturesToAims',
                 ProcessExecutionNode('freesurferGiiTexturesToAims',
                                      optional=1))
  eNode.addLink('RfreesurferGiiTexturesToAims.GiftiCurv',
                'RfreesurferTexturesToGii.GiftiCurv')
  # 14
  eNode.addChild('LfreesurferResamplingDataTextures',
                 ProcessExecutionNode('freesurferResamplingDataTextures',
                                      optional=1))
  eNode.addLink('LfreesurferResamplingDataTextures.OriginalMesh',
                'LfreesurferMessToAimsRef.AimsWhite')
  eNode.addChild('RfreesurferResamplingDataTextures',
                 ProcessExecutionNode('freesurferResamplingDataTextures',
                                      optional=1))
  eNode.addLink('RfreesurferResamplingDataTextures.OriginalMesh',
                'RfreesurferMessToAimsRef.AimsWhite')
  # 15
  eNode.addChild('LfreesurferInflate',
                 ProcessExecutionNode('freesurferInflate',
                                      optional=1))
  eNode.addLink('LfreesurferInflate.White',
                'LfreesurferMessToAimsRef.AimsWhite')
  eNode.addChild('RfreesurferInflate',
                 ProcessExecutionNode('freesurferInflate',
                                      optional=1))
  eNode.addLink('RfreesurferInflate.White',
                'RfreesurferMessToAimsRef.AimsWhite')
  # 16
  eNode.addChild('freesurferConcatenate',
                 ProcessExecutionNode('freesurferConcatenate',
                                      optional=1))
  eNode.addLink('freesurferConcatenate.LeftWhite',
                'LfreesurferMessToAimsRef.AimsWhite')
  # 17
  eNode.addChild('freesurferConcatTex',
                 ProcessExecutionNode('freesurferConcatTex',
                                      optional=1))
  eNode.addLink('freesurferConcatTex.LeftGyri',
                'LfreesurferResampleLabels.ResampledGyri')
  # 18
  self.setExecutionNode( eNode )


