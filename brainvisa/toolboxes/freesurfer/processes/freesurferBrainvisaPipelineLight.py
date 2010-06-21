from neuroProcesses import *

name = 'Brainvisa Freesurfer Pipeline Light'
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

  self.linkParameters( 'rightPial', 'anat' )
  self.linkParameters( 'rightWhite', 'anat' )
  self.linkParameters( 'rightSphereReg', 'anat' )
  self.linkParameters( 'rightThickness', 'anat' )
  self.linkParameters( 'rightCurv', 'anat' )
  self.linkParameters( 'rightAvgCurv', 'anat' )
  self.linkParameters( 'rightCurvPial', 'anat' )
  self.linkParameters( 'rightGyri', 'anat' )

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
  eNode.addLink('LfreesurferMeshResampling.Isin',
                'LfreesurferIsinComputing.Isin')

  eNode.addChild('RfreesurferMeshResampling',
                 ProcessExecutionNode('freesurferMeshResampling',
                                      optional=1))
  eNode.addLink('RfreesurferMeshResampling.PialMesh',
                'RfreesurferConversionGiiMeshToAims.PialMesh')
  eNode.addLink('RfreesurferMeshResampling.Isin',
                'RfreesurferIsinComputing.Isin')
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
  # 18
  self.setExecutionNode( eNode )


