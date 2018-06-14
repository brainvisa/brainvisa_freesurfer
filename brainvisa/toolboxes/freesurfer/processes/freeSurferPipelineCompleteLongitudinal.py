
# -*- coding: utf-8 -*-
from __future__ import print_function

from brainvisa.processes import *

name = 'Freesurfer / BrainVisa full pipeline longitudinal'
userLevel = 3

signature = Signature(
  'RawT1ImageTimepoint1', ReadDiskItem('Raw T1 MRI', 'NIFTI-1 image'),
  'RawT1ImageTimepoint2', ReadDiskItem('Raw T1 MRI', 'NIFTI-1 image'),
  'FSdatabase', Choice()
)


def initialization( self ):
  def fill_databases(proc):
    databases=[h.name for h in neuroHierarchy.hierarchies() if h.fso.name == 'freesurfer']
    proc.signature['FSdatabase'].setChoices(*databases)
    if len( databases ) != 0:
      proc.FSdatabase=databases[0]

  fill_databases(self)

  def linkSubjectName( proc, dummy ):
    if proc.RawT1Image is not None:
      acquisition = proc.RawT1Image.get('acquisition')
      if acquisition is not None:
        return os.path.basename( os.path.dirname( os.path.dirname( os.path.dirname( proc.RawT1Image.fullName() ) ) ) ) + '_acquis_' + acquisition
      print('no acquisition for RawT1Image:', proc.RawT1Image)
  #self.linkParameters( 'subjectName', 'RawT1Image', linkSubjectName )
  def linkAnatImage( proc, dummy ):
    if proc.subjectName is not None and proc.database is not None:
      subject = proc.subjectName
      dirname = proc.database
      filename = os.path.join( dirname, subject, 'mri/orig/001.mgz' )
      return filename
#  #self.linkParameters( 'AnatImage', ( 'subjectName', 'database' ), linkAnatImage )

  eNode = SerialExecutionNode( self.name, parameterized=self )

  eNode1 = ParallelExecutionNode( 'FreeSurfer Cross-Sectional Pipeline', parameterized=self)
  #01 Create Freesurfer subject from T1 anatomical image
  eNode1.addChild( 'FreeSurferSubjectTp1',
                  ProcessExecutionNode( 'freesurferPipelineComplete',
                  optional = 1 ) )
  eNode1.FreeSurferSubjectTp1._process.name = 'Cross-sectional Timepoint 1'
  eNode1.FreeSurferSubjectTp1.signature['FSdatabase'] = Choice()
  fill_databases(eNode1.FreeSurferSubjectTp1)

  eNode1.addChild( 'FreeSurferSubjectTp2',
                  ProcessExecutionNode( 'freesurferPipelineComplete',
                  optional = 1 ) )
  eNode1.FreeSurferSubjectTp2._process.name = 'Cross-sectional Timepoint 2'
  eNode1.FreeSurferSubjectTp2.signature['FSdatabase'] = Choice()
  fill_databases(eNode1.FreeSurferSubjectTp2)
  eNode.addChild('FreeSurferCrossSectional', eNode1)

  eNode.addChild( 'FreeSurferAverageSubjectLongitudinal01',
                  ProcessExecutionNode( 'freesurferAverageSubjectLongitudinal',
                  optional = 1 ) )

  eNode2 = ParallelExecutionNode('FreeSurfer Longitudinal Pipeline')

  eNode2.addChild('FreeSurferLongitudinalTp1',
                 ProcessExecutionNode('freesurferLongitudinalPipeline',
                 optional = 1))
  eNode2.FreeSurferLongitudinalTp1._process.name = 'Longitudinal Timepoint 1'

  eNode2.addChild('FreeSurferLongitudinalTp2',
                 ProcessExecutionNode('freesurferLongitudinalPipeline',
                 optional = 1))
  eNode2.FreeSurferLongitudinalTp2._process.name = 'Longitudinal Timepoint 2'


  eNode.addChild('FreeSurferLongitudinal', eNode2)

  eNode1.FreeSurferSubjectTp1.FreeSurfer01.removeLink( 'subjectName',
                                       'RawT1Image' )
  eNode1.FreeSurferSubjectTp2.FreeSurfer01.removeLink( 'subjectName',
                                        'RawT1Image' )
  eNode1.FreeSurferSubjectTp1.FreeSurfer01.removeLink( 'AnatImage',
                                       'subjectName' )
  eNode1.FreeSurferSubjectTp2.FreeSurfer01.removeLink( 'AnatImage',
                                       'subjectName' )

  eNode1.addDoubleLink('RawT1ImageTimepoint1', 'FreeSurferSubjectTp1.RawT1Image')
  eNode1.addDoubleLink('RawT1ImageTimepoint2', 'FreeSurferSubjectTp2.RawT1Image')

  eNode.addDoubleLink('FreeSurferCrossSectional.FreeSurferSubjectTp1.FreeSurfer01.AnatImage', 'FreeSurferAverageSubjectLongitudinal01.AnatImageTimepoint1')
  eNode.addDoubleLink('FreeSurferCrossSectional.FreeSurferSubjectTp2.FreeSurfer01.AnatImage', 'FreeSurferAverageSubjectLongitudinal01.AnatImageTimepoint2')

  eNode.addDoubleLink('FreeSurferAverageSubjectLongitudinal01.AnatImageTimepoint1', 'FreeSurferLongitudinal.FreeSurferLongitudinalTp1.AnatImageTimepoint')
  eNode.addDoubleLink('FreeSurferAverageSubjectLongitudinal01.AnatImageTimepoint2', 'FreeSurferLongitudinal.FreeSurferLongitudinalTp2.AnatImageTimepoint')
  eNode.addDoubleLink('FreeSurferAverageSubjectLongitudinal01.AnatImage', 'FreeSurferLongitudinal.FreeSurferLongitudinalTp1.AnatImageTemplate')
  eNode.addDoubleLink('FreeSurferAverageSubjectLongitudinal01.AnatImage', 'FreeSurferLongitudinal.FreeSurferLongitudinalTp2.AnatImageTemplate')

  print(eNode.child('FreeSurferCrossSectional').child('FreeSurferSubjectTp1').child('FreeSurfer01').signature)
  #print(eNode.child('FreeSurferLongitudinal').child('FreeSurferLongitudinalTp1').signature)
  eNode.addDoubleLink('FreeSurferCrossSectional.FreeSurferSubjectTp1.FSdatabase', 'FSdatabase')
  eNode.addDoubleLink('FreeSurferCrossSectional.FreeSurferSubjectTp2.FSdatabase', 'FSdatabase')
  eNode.FreeSurferCrossSectional.FreeSurferSubjectTp1.addDoubleLink('FSdatabase', 'FreeSurfer01.database')
  eNode.FreeSurferCrossSectional.FreeSurferSubjectTp2.addDoubleLink('FSdatabase', 'FreeSurfer01.database')


  eNode1.FreeSurferSubjectTp1.FreeSurfer01.linkParameters('subjectName', 'RawT1Image', linkSubjectName)
  eNode1.FreeSurferSubjectTp1.FreeSurfer01.linkParameters('AnatImage', 'subjectName', linkAnatImage)
  eNode1.FreeSurferSubjectTp2.FreeSurfer01.linkParameters('subjectName', 'RawT1Image', linkSubjectName)
  eNode1.FreeSurferSubjectTp2.FreeSurfer01.linkParameters('AnatImage', 'subjectName', linkAnatImage)


  self.setExecutionNode( eNode )


