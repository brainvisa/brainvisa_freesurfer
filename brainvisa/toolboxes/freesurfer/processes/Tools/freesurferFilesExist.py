# -*- coding: utf-8 -*-
import os
from brainvisa.processes import *

name = 'Check Freesurfer files'
userLevel = 1

signature = Signature(
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
  self.linkParameters( 'leftWhite', 'leftPial' )
  self.linkParameters( 'leftSphereReg', 'leftPial' )
  self.linkParameters( 'leftThickness', 'leftPial' )
  self.linkParameters( 'leftCurv', 'leftPial' )
  self.linkParameters( 'leftAvgCurv', 'leftPial' )
  self.linkParameters( 'leftCurvPial', 'leftPial' )
  self.linkParameters( 'leftGyri', 'leftPial' )
  self.linkParameters( 'leftSulciGyri', 'leftPial' )

  self.linkParameters( 'rightPial', 'leftPial' )
  self.linkParameters( 'rightWhite', 'rightPial' )
  self.linkParameters( 'rightSphereReg', 'rightPial' )
  self.linkParameters( 'rightThickness', 'rightPial' )
  self.linkParameters( 'rightCurv', 'rightPial' )
  self.linkParameters( 'rightAvgCurv', 'rightPial' )
  self.linkParameters( 'rightCurvPial', 'rightPial' )
  self.linkParameters( 'rightGyri', 'rightPial' )
  self.linkParameters( 'rightSulciGyri', 'rightPial' )

  #self.linkParameters( 'bv_anat', 'leftPial' )
  #self.linkParameters( 'bv_anat', 'rightPial' )
  
def execution( self, context ):
  context.write( 'Test if all Freesurfer files are present.' )
  if os.path.exists(self.leftPial.fullPath()):
    context.write( self.leftPial.fullPath() + " - " + str(os.path.exists(self.leftPial.fullPath())))
  else:
    context.error( self.leftPial.fullPath() + " - " + str(os.path.exists(self.leftPial.fullPath())))
  if os.path.exists(self.leftWhite.fullPath()):
    context.write( self.leftWhite.fullPath() + " - " + str(os.path.exists(self.leftWhite.fullPath())))
  else:
    context.error( self.leftWhite.fullPath() + " - " + str(os.path.exists(self.leftWhite.fullPath())))
  if os.path.exists(self.leftSphereReg.fullPath()):
    context.write( self.leftSphereReg.fullPath() + " - " + str(os.path.exists(self.leftSphereReg.fullPath())))
  else:
    context.error( self.leftSphereReg.fullPath() + " - " + str(os.path.exists(self.leftSphereReg.fullPath())))
  if os.path.exists(self.leftThickness.fullPath()):
    context.write( self.leftThickness.fullPath() + " - " + str(os.path.exists(self.leftThickness.fullPath())))
  else:
    context.error( self.leftThickness.fullPath() + " - " + str(os.path.exists(self.leftThickness.fullPath())))
  if os.path.exists(self.leftCurv.fullPath()):
    context.write( self.leftCurv.fullPath() + " - " + str(os.path.exists(self.leftCurv.fullPath())))
  else:
    context.error( self.leftCurv.fullPath() + " - " + str(os.path.exists(self.leftCurv.fullPath())))
  if os.path.exists(self.leftAvgCurv.fullPath()):
    context.write( self.leftAvgCurv.fullPath() + " - " + str(os.path.exists(self.leftAvgCurv.fullPath())))
  else:
    context.error( self.leftAvgCurv.fullPath() + " - " + str(os.path.exists(self.leftAvgCurv.fullPath())))
  if os.path.exists(self.leftCurvPial.fullPath()):
    context.write( self.leftCurvPial.fullPath() + " - " + str(os.path.exists(self.leftCurvPial.fullPath())))
  else:
    context.error( self.leftCurvPial.fullPath() + " - " + str(os.path.exists(self.leftCurvPial.fullPath())))
  if os.path.exists(self.leftGyri.fullPath()):
    context.write( self.leftGyri.fullPath() + " - " + str(os.path.exists(self.leftGyri.fullPath())))
  else:
    context.error( self.leftGyri.fullPath() + " - " + str(os.path.exists(self.leftGyri.fullPath())))
  if os.path.exists(self.leftSulciGyri.fullPath()):
    context.write( self.leftSulciGyri.fullPath() + " - " + str(os.path.exists(self.leftSulciGyri.fullPath())))
  else:
    context.error( self.leftSulciGyri.fullPath() + " - " + str(os.path.exists(self.leftSulciGyri.fullPath())))




  if os.path.exists(self.rightPial.fullPath()):
    context.write( self.rightPial.fullPath() + " - " + str(os.path.exists(self.rightPial.fullPath())))
  else:
    context.error( self.rightPial.fullPath() + " - " + str(os.path.exists(self.rightPial.fullPath())))
  if os.path.exists(self.rightWhite.fullPath()):
    context.write( self.rightWhite.fullPath() + " - " + str(os.path.exists(self.rightWhite.fullPath())))
  else:
    context.error( self.rightWhite.fullPath() + " - " + str(os.path.exists(self.rightWhite.fullPath())))
  if os.path.exists(self.rightSphereReg.fullPath()):
    context.write( self.rightSphereReg.fullPath() + " - " + str(os.path.exists(self.rightSphereReg.fullPath())))
  else:
    context.error( self.rightSphereReg.fullPath() + " - " + str(os.path.exists(self.rightSphereReg.fullPath())))
  if os.path.exists(self.rightThickness.fullPath()):
    context.write( self.rightThickness.fullPath() + " - " + str(os.path.exists(self.rightThickness.fullPath())))
  else:
    context.error( self.rightThickness.fullPath() + " - " + str(os.path.exists(self.rightThickness.fullPath())))
  if os.path.exists(self.rightCurv.fullPath()):
    context.write( self.rightCurv.fullPath() + " - " + str(os.path.exists(self.rightCurv.fullPath())))
  else:
    context.error( self.rightCurv.fullPath() + " - " + str(os.path.exists(self.rightCurv.fullPath())))
  if os.path.exists(self.rightAvgCurv.fullPath()):
    context.write( self.rightAvgCurv.fullPath() + " - " + str(os.path.exists(self.rightAvgCurv.fullPath())))
  else:
    context.error( self.rightAvgCurv.fullPath() + " - " + str(os.path.exists(self.rightAvgCurv.fullPath())))
  if os.path.exists(self.rightCurvPial.fullPath()):
    context.write( self.rightCurvPial.fullPath() + " - " + str(os.path.exists(self.rightCurvPial.fullPath())))
  else:
    context.error( self.rightCurvPial.fullPath() + " - " + str(os.path.exists(self.rightCurvPial.fullPath())))
  if os.path.exists(self.rightGyri.fullPath()):
    context.write( self.rightGyri.fullPath() + " - " + str(os.path.exists(self.rightGyri.fullPath())))
  else:
    context.error( self.rightGyri.fullPath() + " - " + str(os.path.exists(self.rightGyri.fullPath())))
  if os.path.exists(self.rightSulciGyri.fullPath()):
    context.write( self.rightSulciGyri.fullPath() + " - " + str(os.path.exists(self.rightSulciGyri.fullPath())))
  else:
    context.error( self.rightSulciGyri.fullPath() + " - " + str(os.path.exists(self.rightSulciGyri.fullPath())))



#  if os.path.exists(self.bv_anat.fullPath()):
#    context.write( self.bv_anat.fullPath() + " - " + str(os.path.exists(self.bv_anat.fullPath())))
#  else:
#    context.error( self.bv_anat.fullPath() + " - " + str(os.path.exists(self.bv_anat.fullPath())))



