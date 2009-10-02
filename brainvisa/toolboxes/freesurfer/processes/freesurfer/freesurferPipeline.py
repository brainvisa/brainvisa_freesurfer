import os
from neuroProcesses import *
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand

name = "02 Launch Freesurfer full pipeline"
userLevel = 2

signature = Signature(
  'AnatImage', ReadDiskItem('FreesurferAnat', 'FreesurferMGZ'),
  )

def initialization(self):
  databases=[(h.name, h) for h in reversed(neuroHierarchy.hierarchies())]# reverse order of hierarchies to have brainvisa shared hierarchy at the end of the list
  self.database=databases[0][1] 
  
def execution(self, context):
  context.write('Launch the Freesurfer pipeline on subject ' + self.AnatImage.get('subject'))
  context.write('recon-all -autorecon-all -subjid %s'%self.AnatImage.get('subject'))

  launchFreesurferCommand(context, self.database.name, 'recon-all', '-autorecon-all',
                          '-subjid', self.AnatImage.get('subject'))
  
  #context.system('echo', 'recon-all', '-autorecon-all', '-subjid', self.AnatImage.get('subject'))
