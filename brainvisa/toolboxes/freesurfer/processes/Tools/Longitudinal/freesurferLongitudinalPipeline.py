

# -*- coding: utf-8 -*-
import os
from brainvisa.processes import *
from freesurfer.brainvisaFreesurfer \
  import launchFreesurferCommand, testFreesurferCommand

name = "Individual Longitudinal Pipeline"
userLevel = 3

def validation():
  testFreesurferCommand()

signature = Signature(
  'AnatImageTimepoint', ReadDiskItem('RawFreesurferAnat', 'FreesurferMGZ'),
  'AnatImageTemplate', ReadDiskItem('T1 FreesurferAnat', 'FreesurferMGZ'),
  'Add_options', String(),
  'subject_tp', String(),
  'subject_template', String(),
  'db', ReadDiskItem('Directory', 'Directory')

  )

def initialization(self):
  def linkSubjectName(param, proc, dummy):
    if self.__dict__[param] is not None:
      subject = self.__dict__[param].get('subject')
      return subject
  #def linkSubjectNames(proc, dummy):
    #if proc.AnatImageTimepoint is not None and proc.AnatImageTemplate is not None and\
        #proc.AnatImageTimepoint.get('subject') is not None and\
        #proc.AnatImageTemplate.get('subject') is not None :
      #proc.subject_tp = proc.AnatImageTimepoint.get('subject')
      #proc.subject_template = proc.AnatImageTemplate.get('subject')
      #return proc.subject_tp

  def linkDB(proc, dummy):
    if proc.AnatImageTimepoint is not None and proc.AnatImageTimepoint.get('_database') is not None:
        proc.db = self.AnatImageTimepoint.get('_database')
        return proc.db

  self.setOptional('Add_options')
  self.setOptional('AnatImageTemplate')
  self.linkParameters('subject_tp', 'AnatImageTimepoint',
                      partial(linkSubjectName, 'AnatImageTimepoint'))
  self.linkParameters('subject_template', 'AnatImageTemplate',
                      partial(linkSubjectName, 'AnatImageTemplate'))
  #self.linkParameters('subject_tp', ('AnatImageTimepoint', 'AnatImageTemplate'), linkSubjectNames)
  self.linkParameters('db', 'AnatImageTimepoint', linkDB)
  self.signature['subject_tp'].userLevel = 3
  self.signature['subject_template'].userLevel = 3
  self.signature['db'].userLevel = 3

def execution(self, context):
  subject_tp = self.subject_tp #self.AnatImageTimepoint.get('subject')
  if subject_tp is None:
    subject_tp = os.path.basename( os.path.dirname( os.path.dirname( os.path.dirname( self.AnatImageTimepoint.fullPath() ) ) ) )
  subject_template = self.subject_template #self.AnatImageTemplate.get('subject')
  context.write('Launch the Freesurfer longitudinal pipeline on subject timepoint ' + subject_tp + ' template ' + subject_template )
  database = self.db.fullPath() #self.AnatImageTimepoint.get('_database')
  if not database:
    database = os.path.dirname( os.path.dirname( os.path.dirname( os.path.dirname( self.AnatImage.fullPath() ) ) ) )


  context.write('recon-all -long %s %s -all'%(subject_template, subject_tp))

  #launchFreesurferCommand(context, database, args)
  kwargs={}
  args = ['recon-all', '-long', subject_tp, subject_template, '-all']
  if self.Add_options is not None :
    liste_option = string.split(self.Add_options)
    for option in liste_option :
      args.append(option)

  launchFreesurferCommand(context, database, *args, **kwargs)
  #launchFreesurferCommand(context, database, 'recon-all', '-autorecon-all', '-subjid', subject, **kwargs )
  #launchFreesurferCommand(context, database, 'recon-all', '-autorecon-all', '-subjid', subject )

#  neuroHierarchy.databases.update( [ os.path.join( database, subject ) ] )

