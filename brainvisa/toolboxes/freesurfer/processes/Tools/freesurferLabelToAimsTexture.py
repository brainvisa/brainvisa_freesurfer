# -*- coding: utf-8 -*-
from brainvisa.processes import *
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand
from glob import glob

name = '09/10 Converting freesurfer unreadable labels to aims textures.'
userlevel = 2

signature = Signature(
  'WhiteMesh', ReadDiskItem('White', 'Aims mesh formats', enableConversion=0),
  'Gyri', ReadDiskItem('FreesurferGyriTexture', 'FreesurferParcellation'),
  'SulciGyri', ReadDiskItem('FreesurferSulciGyriTexture', 'FreesurferParcellation'),
#  'Gyri', ReadDiskItem('FreesurferReadableGyriTexture', 'Series of FreesurferLabel'),
#  'SulciGyri', ReadDiskItem('FreesurferReadableSulciGyriTexture', 'Series of FreesurferLabel'),
  'GyriTexture', WriteDiskItem('FreesurferGyri', 'Aims Texture formats'),
  'SulciGyriTexture', WriteDiskItem('FreesurferSulciGyri', 'Aims Texture formats'),
  'side', Choice( ( 'left', 'lh' ), ( 'right', 'rh' ), None ),
  'database', ReadDiskItem( 'Directory', 'Directory' ),
  'subject', String(),
  )

def initialization(self):
  def linkside( self, dummy ):
    if self.Gyri is not None:
      return self.Gyri.get( 'side' )
  def linkDB( self, dummy ):
    if self.Gyri:
      return self.Gyri.get('_database')
  def linkSubject( self, dummy ):
    if self.Gyri:
      return self.Gyri.get('subject')

  self.linkParameters('Gyri', 'WhiteMesh')
  self.linkParameters('SulciGyri', 'WhiteMesh')
  self.linkParameters('GyriTexture', 'WhiteMesh')
  self.linkParameters('SulciGyriTexture', 'WhiteMesh')
  self.linkParameters('side', 'Gyri', linkside )
  self.linkParameters('database', 'Gyri', linkDB )
  self.linkParameters('subject', 'Gyri', linkSubject )
  self.signature[ 'side' ].userLevel = 2
  self.signature[ 'database' ].userLevel = 2
  self.signature[ 'subject' ].userLevel = 2


def execution(self, context):
  context.write('Conversion of freesurfer labels to aims labels.')

  side = self.side
  print 'side:', side
  print 'subject:', self.subject

  launchFreesurferCommand(context,
                          self.database.fullPath(),
                          'mri_annotation2label',
                          '--subject', self.subject,
                          '--hemi', side,
                          '--annotation', self.Gyri.fullName()[self.Gyri.fullName().rfind('/')+4:],
                          '--labelbase', self.Gyri.fullPath()[self.Gyri.fullPath().rfind('/')+1:])
  gyriFiles = sorted( glob( self.Gyri.fullPath() + '-*.label' ) )
  launchFreesurferCommand(context,
                          self.database.fullPath(),
                          'mri_annotation2label',
                          '--subject', self.subject,
                          '--hemi', side,
                          '--annotation', self.SulciGyri.fullName()[self.SulciGyri.fullName().rfind('/')+4:],
                          '--labelbase', self.SulciGyri.fullPath()[self.SulciGyri.fullPath().rfind('/')+1:])
  sulciGyriFiles = sorted( glob( self.SulciGyri.fullPath() + '-*.label' ) )


  # GYRI PART
  context.write("---Gyri---")
  if gyriFiles:
    context.system('python', '-c', 'from freesurfer.freesurferTexture2Tex import freesurferTexture2TexBrainvisa as f; f(%s, \"%s\", \"%s\");'%(gyriFiles, self.WhiteMesh.fullPath(), self.GyriTexture.fullPath()))
  else:
    context.write("no gyri file, conversion from freesurfer failed")
  for i in gyriFiles:
    os.remove( i )
  
  # SULCI-GYRI PART
  context.write("---Sulci-Gyri---")
  if sulciGyriFiles:
    context.system('python', '-c', 'from freesurfer.freesurferTexture2Tex import freesurferTexture2TexBrainvisa as f; f(%s, \"%s\", \"%s\");'%(sulciGyriFiles, self.WhiteMesh.fullPath(), self.SulciGyriTexture.fullPath()))
  else:
    context.write("no sulci-gyri file, conversion from freesurfer failed")
  for i in sulciGyriFiles:
    os.remove( i )

 



