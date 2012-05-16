import os
from brainvisa.processes import *
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand

name = "01 Create Freesurfer subject from Dicom anatomical image"
userLevel = 2

signature = Signature(
  'DicomImage', ReadDiskItem('Any Type', getAllFormats()),
  'subjectName', String(),
  'database', Choice(),
  )

def initialization(self):
  databases=[(h.name, h) for h in reversed(neuroHierarchy.hierarchies())]# reverse order of hierarchies to have brainvisa shared hierarchy at the end of the list
  self.signature['database'].setChoices(*databases)
  self.database=databases[0][1] 

  
def execution(self, context):
  context.write('Create subject hierarchy and convert Dicom image to mgz format.')
  cmd = 'recon-all -i %s -subjid %s'%(self.DicomImage.fullPath(), self.subjectName)
  context.write(cmd)
  context.write(self.database.name)
  launchFreesurferCommand(context, self.database.name, 'recon-all', '-i', self.DicomImage.fullPath(), '-subjid', self.subjectName)
  createdDir = self.database.name+'/'+self.subjectName
  context.write("Updating database, path = " + createdDir)
  neuroHierarchy.databases.update([createdDir])
  #neuroHierarchy.databases.update()
  


