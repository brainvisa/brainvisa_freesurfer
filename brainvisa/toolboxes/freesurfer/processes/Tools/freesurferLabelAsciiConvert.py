# -*- coding: utf-8 -*-
from __future__ import absolute_import
from brainvisa.processes import *
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand

name = '09 Converting labels to readable ascii format.'
userlevel = 2

signature = Signature(
    'Gyri', ReadDiskItem('FreesurferGyriTexture', 'FreesurferParcellation'),
  'SulciGyri', ReadDiskItem(
      'FreesurferSulciGyriTexture', 'FreesurferParcellation'),
  'side', Choice(('left', 'lh'), ('right', 'rh'), None),
  'database', ReadDiskItem('Directory', 'Directory'),
  'subject', String(),
)


def initialization(self):
    def linkside(self, dummy):
        if self.Gyri is not None:
            return self.Gyri.get('side')

    def linkDB(self, dummy):
        if self.Gyri:
            return self.Gyri.get('_database')

    def linkSubject(self, dummy):
        if self.Gyri:
            return self.Gyri.get('subject')

    self.linkParameters('SulciGyri', 'Gyri')
    self.linkParameters('side', 'Gyri', linkside)
    self.linkParameters('database', 'Gyri', linkDB)
    self.linkParameters('subject', 'Gyri', linkSubject)
    self.signature['side'].userLevel = 2
    self.signature['database'].userLevel = 2
    self.signature['subject'].userLevel = 2


def execution(self, context):
    context.write('Resample brain mesh.')
    side = self.side

    context.write('mri_annotation2label --subject %s --hemi %s --annotation %s --labelbase %s' %
                  (self.subject, side, self.Gyri.fullName()[self.Gyri.fullName().rfind('/') + 4:], self.Gyri.fullPath()[self.Gyri.fullPath().rfind('/') + 1:]))

    launchFreesurferCommand(context,
                            self.database.fullPath(),
                            'mri_annotation2label',
                            '--subject', self.subject,
                            '--hemi', side,
                            '--annotation', self.Gyri.fullName()[
                            self.Gyri.fullName(
                            ).rfind(
                            '/') + 4:],
                            '--labelbase', self.Gyri.fullPath()[self.Gyri.fullPath().rfind('/') + 1:])

    context.write('mri_annotation2label --subject %s --hemi %s --annotation %s --labelbase %s' %
                  (self.subject, side, self.SulciGyri.fullName()[self.SulciGyri.fullName().rfind('/') + 4:], self.SulciGyri.fullPath()[self.SulciGyri.fullPath().rfind('/') + 1:]))

    launchFreesurferCommand(context,
                            self.database.fullPath(),
                            'mri_annotation2label',
                            '--subject', self.subject,
                            '--hemi', side,
                            '--annotation', self.SulciGyri.fullName()[
                            self.SulciGyri.fullName(
                            ).rfind(
                            '/') + 4:],
                            '--labelbase', self.SulciGyri.fullPath()[self.SulciGyri.fullPath().rfind('/') + 1:])
