# -*- coding: utf-8 -*-
from brainvisa.processes import *
from brainvisa.group_utils import Subject
from soma.minf.api import registerClass, writeMinf

name = '1 Creation of a group of subject'
userLevel = 1

signature = Signature(
  'list_of_subjects',ListOf ( ReadDiskItem("Subject", 'Directory') ),
  'group_definition', WriteDiskItem('Freesurfer Group definition', 'XML' ),
);

def initialization(self):
  pass



def execution(self, context):
  context.runProcess( 'createGroup', self.list_of_subjects,
    self.group_definition )

