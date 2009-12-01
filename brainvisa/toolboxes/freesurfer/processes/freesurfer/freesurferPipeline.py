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
  context.write('recon-all -autorecon-all -subjid %s'%self.AnatImage.get('subject'))
  database = self.AnatImage.get('_database')
  subject = self.AnatImage.get('subject')
  context.write('/home/at215559/cpfreesurfer.bash' + ' ' + subject + ' ' + database)
  context.system('/home/at215559/cpfreesurfer.bash', subject, database)
  neuroHierarchy.databases.update([database+'/'+subject])
  #launchFreesurferCommand(context, self.database, 'recon-all', '-autorecon-all',
  #                        '-subjid', self.AnatImage.get('subject'))
  
  #context.system('echo', 'recon-all', '-autorecon-all', '-subjid', self.AnatImage.get('subject'))
