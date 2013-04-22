
# -*- coding: utf-8 -*-
import os
from brainvisa.processes import *
from freesurfer.brainvisaFreesurfer \
  import launchFreesurferCommand, testFreesurferCommand
import string

name = "Average Subject Longitudinal Pipeline"
userLevel = 3

def validation():
  testFreesurferCommand()

signature = Signature(
  'AnatImageTimepoint1', ReadDiskItem('RawFreesurferAnat', 'FreesurferMGZ'),
  'AnatImageTimepoint2', ReadDiskItem('RawFreesurferAnat', 'FreesurferMGZ'),
  'template_name', String(),
  'AnatImage', WriteDiskItem('RawFreesurferAnat', 'FreesurferMGZ'),
  'Add_options', String(),

  #liens non visible:
  'leftPial', WriteDiskItem('BaseFreesurferType', 'FreesurferPial',
         requiredAttributes = {'side': 'left'}),
  'leftWhite', WriteDiskItem('BaseFreesurferType', 'FreesurferWhite',
         requiredAttributes = {'side': 'left'}),
  'leftSphereReg', WriteDiskItem('BaseFreesurferType', 'FreesurferSphereReg',
         requiredAttributes = {'side': 'left'}),
  'leftThickness', WriteDiskItem('BaseFreesurferType', 'FreesurferThickness',
         requiredAttributes = {'side': 'left'}),
  'leftCurv', WriteDiskItem('BaseFreesurferType', 'FreesurferCurv',
         requiredAttributes = {'side': 'left'}),
  'leftAvgCurv', WriteDiskItem('BaseFreesurferType', 'FreesurferAvgCurv',
         requiredAttributes = {'side': 'left'}),
  'leftCurvPial', WriteDiskItem('BaseFreesurferType', 'FreesurferCurvPial',
         requiredAttributes = {'side': 'left'}),
  'leftGyri', WriteDiskItem('FreesurferGyriTexture', 'FreesurferParcellation',
         requiredAttributes = {'side': 'left'}),
  'leftSulciGyri',
         WriteDiskItem('FreesurferSulciGyriTexture', 'FreesurferParcellation',
         requiredAttributes = {'side': 'left'}),

  'rightPial', WriteDiskItem('BaseFreesurferType', 'FreesurferPial',
         requiredAttributes = {'side': 'right'}),
  'rightWhite', WriteDiskItem('BaseFreesurferType', 'FreesurferWhite',
         requiredAttributes = {'side': 'right'}),
  'rightSphereReg', WriteDiskItem('BaseFreesurferType', 'FreesurferSphereReg',
         requiredAttributes = {'side': 'right'}),
  'rightThickness', WriteDiskItem('BaseFreesurferType', 'FreesurferThickness',
         requiredAttributes = {'side': 'right'}),
  'rightCurv', WriteDiskItem('BaseFreesurferType', 'FreesurferCurv',
         requiredAttributes = {'side': 'right'}),
  'rightAvgCurv', WriteDiskItem('BaseFreesurferType', 'FreesurferAvgCurv',
         requiredAttributes = {'side': 'right'}),
  'rightCurvPial', WriteDiskItem('BaseFreesurferType', 'FreesurferCurvPial',
         requiredAttributes = {'side': 'right'}),
  'rightGyri', WriteDiskItem('FreesurferGyriTexture', 'FreesurferParcellation',
         requiredAttributes = {'side': 'right'}),
  'rightSulciGyri',
         WriteDiskItem('FreesurferSulciGyriTexture', 'FreesurferParcellation',
         requiredAttributes = {'side': 'right'}),

  'subject_tp1', String(),
  'subject_tp2', String(),
  'db', ReadDiskItem('Directory', 'Directory')

  )

def initialization(self):
#  def linkTemplateName( proc, dummy ):
#    if proc.AnatImageTimepoint1 is not None and proc.AnatImageTimepoint2 is not None:
#      print proc.AnatImageTimepoint1.get('subject')
#      print proc.AnatImageTimepoint1
#      subject_tp1, timepoint1 = string.split(proc.AnatImageTimepoint1.get('subject'), '_acquis_')
#      subject_tp2, timepoint2 = string.split(proc.AnatImageTimepoint2.get('subject'), '_acquis_')
#      assert(subject_tp1 == subject_tp2)
#      subject_ave = subject_tp1 + '_template'
#      return proc.AnatImageTimepoint1

  def linkAnatImageName( proc, dummy):
    if proc.AnatImageTimepoint1 is not None and proc.AnatImageTimepoint1.get('_database') is not None and proc.template_name is not None:
      subject = proc.template_name
      dirname = proc.AnatImageTimepoint1.get('_database')
      filename = os.path.join( dirname, subject, 'mri/orig/001.mgz' )
      return filename

  def linkSubjectNames( proc, dummy):
    if proc.AnatImageTimepoint1 is not None and proc.AnatImageTimepoint2 is not None and\
        proc.AnatImageTimepoint1.get('subject') is not None and proc.AnatImageTimepoint2.get('subject') is not None:
        proc.subject_tp1 = proc.AnatImageTimepoint1.get('subject')
        proc.subject_tp2 = proc.AnatImageTimepoint2.get('subject')
        print 'toto', proc.subject_tp1
        subject_tp1, timepoint1 = string.split(str(proc.subject_tp1), '_acquis_')
        subject_tp2, timepoint2 = string.split(str(proc.subject_tp2), '_acquis_')
        assert(subject_tp1 == subject_tp2)
        subject_ave = subject_tp1 + '_template_' + str(proc.subject_tp1) + '_versus_' + str(proc.subject_tp2)
        proc.template_name = subject_ave
        print proc.template_name
        return proc.template_name

  def linkDB( proc, dummy):
    if proc.AnatImage is not None:
        proc.db = proc.AnatImage.get('_database')
        return proc.db

  self.setOptional('Add_options')

  self.linkParameters( 'template_name', ('AnatImageTimepoint1', 'AnatImageTimepoint2'), linkSubjectNames)
  self.linkParameters( 'AnatImage', ('template_name', 'AnatImageTimepoint1'), linkAnatImageName)
  self.linkParameters( 'db', 'AnatImage' , linkDB)
  self.linkParameters( 'leftPial', 'AnatImage' )
  self.linkParameters( 'leftWhite', 'AnatImage' )
  self.linkParameters( 'leftSphereReg', 'AnatImage' )
  self.linkParameters( 'leftThickness', 'AnatImage' )
  self.linkParameters( 'leftCurv', 'AnatImage' )
  self.linkParameters( 'leftAvgCurv', 'AnatImage' )
  self.linkParameters( 'leftCurvPial', 'AnatImage' )
  self.linkParameters( 'leftGyri', 'AnatImage' )
  self.linkParameters( 'leftSulciGyri', 'AnatImage' )

  self.linkParameters( 'rightPial', 'AnatImage' )
  self.linkParameters( 'rightWhite', 'AnatImage' )
  self.linkParameters( 'rightSphereReg', 'AnatImage' )
  self.linkParameters( 'rightThickness', 'AnatImage' )
  self.linkParameters( 'rightCurv', 'AnatImage' )
  self.linkParameters( 'rightAvgCurv', 'AnatImage' )
  self.linkParameters( 'rightCurvPial', 'AnatImage' )
  self.linkParameters( 'rightGyri', 'AnatImage' )
  self.linkParameters( 'rightSulciGyri', 'AnatImage' )

  self.signature['leftPial'].userLevel = 3
  self.signature['leftWhite'].userLevel = 3
  self.signature['leftSphereReg'].userLevel = 3
  self.signature['leftThickness'].userLevel = 3
  self.signature['leftCurv'].userLevel = 3
  self.signature['leftAvgCurv'].userLevel = 3
  self.signature['leftCurvPial'].userLevel = 3
  self.signature['leftGyri'].userLevel = 3
  self.signature['leftSulciGyri'].userLevel = 3

  self.signature['rightPial'].userLevel = 3
  self.signature['rightWhite'].userLevel = 3
  self.signature['rightSphereReg'].userLevel = 3
  self.signature['rightThickness'].userLevel = 3
  self.signature['rightCurv'].userLevel = 3
  self.signature['rightAvgCurv'].userLevel = 3
  self.signature['rightCurvPial'].userLevel = 3
  self.signature['rightGyri'].userLevel = 3
  self.signature['rightSulciGyri'].userLevel = 3

  self.signature['subject_tp1'].userLevel = 3
  self.signature['subject_tp2'].userLevel = 3
  self.signature['db'].userLevel = 3

def execution(self, context):
  subject_tp1 = self.subject_tp1 #AnatImageTimepoint1.get('subject')
  if subject_tp1 is None:
    subject_tp1 = os.path.basename( os.path.dirname( os.path.dirname( os.path.dirname( self.AnatImageTimepoint1.fullPath() ) ) ) )
  subject_tp2 = self.subject_tp2 #AnatImageTimepoint1.get('subject')
  if subject_tp2 is None:
    subject_tp2 = os.path.basename( os.path.dirname( os.path.dirname( os.path.dirname( self.AnatImageTimepoint2.fullPath() ) ) ) )
  subject_ave = self.template_name #AnatImage.get('subject')
  context.write('Launch the Freesurfer pipeline on subject timepoints ' + subject_tp1 + subject_tp2 + subject_ave )
  database = self.db.fullPath() #AnatImage.get('_database')
  if not database:
    database = os.path.dirname( os.path.dirname( os.path.dirname( os.path.dirname( self.AnatImage.fullPath() ) ) ) )


  context.write('recon-all -base %s -autorecon-all -tp %s -tp %s'%(subject_ave, subject_tp1, subject_tp2))

  #launchFreesurferCommand(context, database, args)
  kwargs={}
  args = ['recon-all', '-base', subject_ave, '-autorecon-all', '-tp', subject_tp1, '-tp', subject_tp2]
  if self.Add_options is not None :
    liste_option = string.split(self.Add_options)
    for option in liste_option :
      args.append(option)

  launchFreesurferCommand(context, database, *args, **kwargs)
  #launchFreesurferCommand(context, database, 'recon-all', '-autorecon-all', '-subjid', subject, **kwargs )
  #launchFreesurferCommand(context, database, 'recon-all', '-autorecon-all', '-subjid', subject )

#  neuroHierarchy.databases.update( [ os.path.join( database, subject ) ] )

