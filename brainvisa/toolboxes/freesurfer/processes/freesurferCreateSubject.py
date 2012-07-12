import os
from brainvisa.processes import *
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand

name = "01 Create Freesurfer subject from T1 anatomical image"
userLevel = 2

signature = Signature(
  'RawT1Image', ReadDiskItem('Raw T1 MRI', getAllFormats()),
  'subjectName', String(),
  'database', Choice(),
  )

def initialization(self):
  def linkSubjectName( proc, dummy ):
    if proc.RawT1Image is not None:
      return os.path.basename( proc.RawT1Image.fullName() )
  databases=[h.name for h in reversed(neuroHierarchy.hierarchies())]# reverse order of hierarchies to have brainvisa shared hierarchy at the end of the list
  self.signature['database'].setChoices(*databases)
  if len( databases ) != 0:
    self.database=databases[0]
  else:
    self.signature[ 'database' ] = OpenChoice()
  self.linkParameters( 'subjectName', 'RawT1Image', linkSubjectName )

  
def execution(self, context):
  context.write('Create subject hierarchy and convert image to mgz format.')
  cmd = 'recon-all -i %s -subjid %s'%(self.RawT1Image.fullPath(), self.subjectName)
  context.write(cmd)
  context.write(self.database)
  launchFreesurferCommand(context, self.database, 'recon-all', '-i', self.RawT1Image.fullPath(), '-subjid', self.subjectName)
  createdDir = self.database+'/'+self.subjectName
  context.write("Updating database, path = " + createdDir)
  neuroHierarchy.databases.update([createdDir])
  #neuroHierarchy.databases.update()
  


