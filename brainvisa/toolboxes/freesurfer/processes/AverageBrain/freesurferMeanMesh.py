# -*- coding: utf-8 -*-
from brainvisa.processes import *
from brainvisa.group_utils import Subject
from soma.minf.api import registerClass, readMinf

name = '2 Average brain mesh'
userLevel = 1

signature = Signature(
  'group', ReadDiskItem('Freesurfer Group definition', 'XML' ),
  'LeftAverageMesh', WriteDiskItem('AverageBrainWhite', 'MESH mesh',
                                   requiredAttributes = {'side':'left'}),
  'RightAverageMesh', WriteDiskItem('AverageBrainWhite', 'MESH mesh',
                                   requiredAttributes = {'side':'right'}),
  'BothAverageMesh', WriteDiskItem('BothAverageBrainWhite', 'MESH mesh'),
);

def initialization(self):
  self.linkParameters('LeftAverageMesh', 'group')
  self.linkParameters('RightAverageMesh', 'group')
  self.linkParameters('BothAverageMesh', 'group')

def execution(self, context):
  registerClass('minf_2.0', Subject, 'Subject')
  groupOfSubjects = readMinf(self.group.fullPath())

  # Left side
  subjects = []
  rattrs = {'side' : 'left'}
  for subject in groupOfSubjects:
    subjects.append(ReadDiskItem('AimsWhite','MESH mesh').findValue(subject.attributes(), requiredAttributes = rattrs))

  context.write(str([i.fullPath() for i in subjects]))

  context.system('python', '-c', 'from freesurfer.average_mesh import average_mesh as f; f(\"%s\", %s);'%(self.LeftAverageMesh.fullPath(), str([i.fullPath() for i in subjects])))

  # Right side
  subjects = []
  rattrs = {'side' : 'right'}
  for subject in groupOfSubjects:
    subjects.append(ReadDiskItem('AimsWhite','MESH mesh').findValue(subject.attributes(), requiredAttributes = rattrs))

  context.write(str([i.fullPath() for i in subjects]))

  context.system('python', '-c', 'from freesurfer.average_mesh import average_mesh as f; f(\"%s\", %s);'%(self.RightAverageMesh.fullPath(), str([i.fullPath() for i in subjects])))
  
  context.system( 'AimsZCat', '-i', self.LeftAverageMesh.fullPath(),
                  self.RightAverageMesh.fullPath(), '-o',
                  self.BothAverageMesh.fullPath() )
