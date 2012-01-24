# -*- coding: utf-8 -*-
import os
from neuroProcesses import *
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
  context.write('Launch the Freesurfer pipeline on subject ' + self.AnatImage.get('subject'))
  database = self.AnatImage.get('_database')
  subject = self.AnatImage.get('subject')
  context.write('recon-all -autorecon-all -subjid %s'%subject)
  launchFreesurferCommand(context, database, 'recon-all',
    '-autorecon-all', '-subjid', subject )
  neuroHierarchy.databases.update( [ os.path.join( database, subject ) ] )

