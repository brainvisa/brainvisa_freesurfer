# -*- coding: utf-8 -*-

from __future__ import print_function

from __future__ import absolute_import
from brainvisa.processes import *
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand

name = 'Freesurfer aparcstats2table'
userLevel = 0

signature = Signature(
    'anat_images', ListOf(ReadDiskItem(
        'T1 FreesurferAnat',
        ['FreesurferMGZ', 'NIFTI-1 image'])),
    'database', Choice(),
    'subjects', ListOf(String()),
    'hemi_side', Choice(('left', 'lh'),
                        ('right', 'rh')),
    'measures', Choice('area', 'volume',
                       'thickness', 'thicknessstd',
                       'meancurv', 'gauscurv',
                       'foldind', 'curvind'),
    'parcellation', Choice('aparc', 'aparc.a2009s'),
    'skip_subject_with_error', Boolean(),
    'other_options', String(),
    'output_file',  WriteDiskItem(
        'Text file',
        ['Text file', 'CSV file']),
)


def initialization(self):

    databases = [h.name for h in neuroHierarchy.hierarchies()
                 if h.fso.name == 'freesurfer']
    self.signature['database'].setChoices(*databases)
    if len(databases) != 0:
        self.database = databases[0]
    else:
        self.signature["database"] = ReadDiskItem('Directory', 'Directory')

    def linkDB(self, dummy):
        if self.anat_images:
            dbs = [anat.get('_database') for anat in self.anat_images]
            if all(x == dbs[0] for x in dbs):
                return dbs[0]
            else:
                print(
                    'Anat images were selected from two different databases.')

    def linkSubject(self, dummy):
        if self.anat_images:
            subjects = [anat.get('subject') for anat in self.anat_images]
            return subjects

    self.setOptional('anat_images')
    self.setOptional('other_options')
    self.linkParameters('database', 'anat_images', linkDB)
    self.linkParameters('subjects', 'anat_images', linkSubject)


def execution(self, context):

    cmd = ['aparcstats2table',
           '--hemi', self.hemi_side,
           '--meas', self.measures,
           '--parc', self.parcellation,
           '--delimiter', 'comma',
           '--tablefile', self.output_file,
           '--subjects']
    cmd.extend(self.subjects)

    if self.skip_subject_with_error:
        cmd.append('--skip')

    if self.other_options is not None:
        liste_option = self.other_options.split()
        for option in liste_option:
            cmd.append(option)

    context.write(*cmd)
    launchFreesurferCommand(context, self.database, *cmd)
