# -*- coding: utf-8 -*-
import os
from brainvisa.processes import *
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand

name = "02 Launch Freesurfer full pipeline TEST-VERSION"
userLevel = 2

signature = Signature(
  'AnatImage', ReadDiskItem('FreesurferAnat', 'FreesurferMGZ'),
  )

def initialization(self):
  #databases=[(h.name, h) for h in reversed(neuroHierarchy.hierarchies())]# reverse order of hierarchies to have brainvisa shared hierarchy at the end of the list
  #self.database=databases[0][1]
  pass
  
def execution(self, context):
  subject = self.AnatImage.get('subject')
  if subject is None:
    subject = os.path.basename( os.path.dirname( os.path.dirname( os.path.dirname( self.AnatImage.fullPath() ) ) ) )
  context.write('Launch the Freesurfer pipeline on subject ' + subject )
  database = self.AnatImage.get('_database')
  if not database:
    database = os.path.dirname( os.path.dirname( os.path.dirname( os.path.dirname( self.AnatImage.fullPath() ) ) ) )
  context.write('recon-all -autorecon-all -subjid %s'%subject)
  launchFreesurferCommand(context, database, 'recon-all',
    '-autorecon-all', '-subjid', subject )
  neuroHierarchy.databases.update( [ os.path.join( database, subject ) ] )

