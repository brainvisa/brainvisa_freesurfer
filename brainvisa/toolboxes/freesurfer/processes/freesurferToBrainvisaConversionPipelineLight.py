# -*- coding: utf-8 -*-
from brainvisa.processes import *

name = 'Freesurfer outputs To BrainVisa conversion pipeline, Light version'
userLevel = 1

try:
  p = getProcessInstance( 'freesurferBrainvisaPipeline' )

  s = []
  for n in p.signature.sortedKeys:
    s += [ n, p.signature[n] ]
  signature = Signature( *s )
  del s, n, p
except:
  pass

def initialization( self ):
  if len( self.__class__.signature ) == 0:
    p = getProcessInstance( 'freesurferToBrainvisaConversionPipeline' )

    s = []
    for n in p.signature.sortedKeys:
      s += [ n, p.signature[n] ]
    self.__class__.signature = Signature( *s )
    self.changeSignature( self.__class__.signature )
    del s, n
  p = getProcessInstance( 'freesurferToBrainvisaConversionPipeline' )
  if not hasattr( self.__class__, 'initParent' ):
    self.__class__.initParent = p.__class__.initialization.im_func
  self.initParent()
  self.setOptional( 'leftSulciGyri' )
  self.setOptional( 'rightSulciGyri' )
  eNode = self.executionNode()
  eNode.LfreesurferLabelToAimsTexture.setSelected( False )
  eNode.RfreesurferLabelToAimsTexture.setSelected( False )
  eNode.LfreesurferResampleLabels.setSelected( False )
  eNode.RfreesurferResampleLabels.setSelected( False )
  eNode.LfreesurferTexturesToGii.setSelected( False )
  eNode.RfreesurferTexturesToGii.setSelected( False )
  eNode.LfreesurferResamplingDataTextures.setSelected( False )
  eNode.RfreesurferResamplingDataTextures.setSelected( False )
  eNode.freesurferConcatenate.setSelected( False )
  eNode.freesurferConcatTex.setSelected( False )

