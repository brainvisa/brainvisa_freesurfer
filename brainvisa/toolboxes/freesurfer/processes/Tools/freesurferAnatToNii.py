# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys

from __future__ import absolute_import
from brainvisa.processes import *
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand
from brainvisa import registration


name = "Convert Freesurfer images to nifti format"
userLevel = 2


signature = Signature(
    'chosen_format', Choice('gz compressed NIFTI-1 image',
                            'NIFTI-1 image'),
    # Inputs
    'raw', ReadDiskItem(
        'RawFreesurferAnat',
        'FreesurferMGZ',
        enableConversion=False),
    'raw_nifti', WriteDiskItem(
        'RawFreesurferAnat',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image']),
        #_debug=sys.stdout,
        # preferExisting=True),
    'referential', ReadDiskItem(
        'Referential of Raw T1 MRI',
        'Referential'),
    'orig', ReadDiskItem(
        'T1 FreesurferAnat',
        'FreesurferMGZ',
        enableConversion=False,
        exactType=True),
    'orig_nifti', WriteDiskItem(
        'T1 FreesurferAnat',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        exactType=True),
    # Bias correction
    'nu', ReadDiskItem(
        'Nu FreesurferAnat',
        'FreesurferMGZ',
        enableConversion=False),
    'nu_nifti', WriteDiskItem(
        'Nu FreesurferAnat',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image']),
        #_debug=sys.stdout,
        # preferExisting=True),
    # Segmentation
    'ribbon', ReadDiskItem(
        'Ribbon Freesurfer',
        'FreesurferMGZ',
        requiredAttributes={'side': 'both',
                            'space': 'freesurfer analysis'},
        enableConversion=False),
    'ribbon_nifti', WriteDiskItem(
        'Ribbon Freesurfer',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'side': 'both',
                            'space': 'freesurfer analysis'}),
    'aseg', ReadDiskItem(
        'Freesurfer Aseg',
        'FreesurferMGZ',
        requiredAttributes={'space': 'freesurfer analysis'},
        enableConversion=False),
    'aseg_nifti', WriteDiskItem(
        'Freesurfer Aseg',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'space': 'freesurfer analysis'}),
    'aparc_aseg', ReadDiskItem(
        'Freesurfer Cortical Parcellation',
        'FreesurferMGZ',
        requiredAttributes={'atlas': 'Desikan-Killiany',
                            'space': 'freesurfer analysis'},
        enableConversion=False),
    'aparc_aseg_nifti', WriteDiskItem(
        'Freesurfer Cortical Parcellation',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'atlas': 'Desikan-Killiany',
                            'space': 'freesurfer analysis'}),
    'aparc_a2009s_aseg', ReadDiskItem(
        'Freesurfer Cortical Parcellation',
        'FreesurferMGZ',
        requiredAttributes={'atlas': 'Destrieux',
                            'space': 'freesurfer analysis'},
        enableConversion=False),
    'aparc_a2009s_aseg_nifti', WriteDiskItem(
        'Freesurfer Cortical Parcellation',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image'],
        requiredAttributes={'atlas': 'Destrieux',
                            'space': 'freesurfer analysis'}),
)


def updateFormat(self, param1, param2, proc, dummy):
    result = None
    if self.__dict__[param1] is not None:
        fobj = getFormat(self.chosen_format)
        if fobj is None:
            return None
        # I found no method to get the file extension from a format.
        fp = fobj.patterns.patterns[0].pattern.split('|*')
        if len(fp) == 2:
            # print(self.__dict__[param1].fullPath())
            filename = self.__dict__[param1].fullName() + fp[1]
            result = WriteDiskItem(
                param2, self.chosen_format).findValue(filename)
    return result


def initialization(self):
    self.linkParameters('referential', 'raw')
    self.linkParameters('orig', 'raw')
    self.linkParameters('nu', 'orig')
    self.linkParameters('ribbon', 'nu')
    self.linkParameters('aseg', 'nu')
    self.linkParameters('aparc_aseg', 'nu')
    self.linkParameters('aparc_a2009s_aseg', 'nu')

    self.linkParameters('raw_nifti',
                        ['raw', 'chosen_format'],
                        partial(self.updateFormat, 'raw', 'RawFreesurferAnat'))
    self.linkParameters('orig_nifti',
                        ['orig', 'chosen_format'],
                        partial(self.updateFormat, 'orig', 'T1 FreesurferAnat'))
    self.linkParameters('nu_nifti',
                        ['nu', 'chosen_format'],
                        partial(self.updateFormat, 'nu', 'Nu FreesurferAnat'))
    self.linkParameters('ribbon_nifti',
                        ['ribbon', 'chosen_format'],
                        partial(self.updateFormat, 'ribbon', 'Ribbon Freesurfer'))
    self.linkParameters('aseg_nifti',
                        ['aseg', 'chosen_format'],
                        partial(self.updateFormat, 'aseg', 'Freesurfer Aseg'))
    self.linkParameters('aparc_aseg_nifti',
                        ['aparc_aseg', 'chosen_format'],
                        partial(self.updateFormat, 'aparc_aseg', 'Freesurfer Cortical Parcellation'))
    self.linkParameters('aparc_a2009s_aseg_nifti',
                        ['aparc_a2009s_aseg', 'chosen_format'],
                        partial(self.updateFormat, 'aparc_a2009s_aseg', 'Freesurfer Cortical Parcellation'))

    self.chosen_format = 'gz compressed NIFTI-1 image'
    self.setOptional('raw')
    self.setOptional('raw_nifti')
    self.setOptional('referential')


def execution(self, context):
    # Convert from .mgz to .nii using a converter (which can be either aims or
    # the freesurfer mri_convert-based one)
    conv = context.getConverter(self.orig, self.orig_nifti)
    if conv is None:
        raise ValidationError(
            'No converter could be found to convert FreeSurfer MGZ format')
    context.write('converter found:', conv.name)

    if self.raw_nifti:
        if os.path.exists(self.raw_nifti.minfFileName()):
            context.write('removing residual .minf file %s' %
                          self.raw_nifti.minfFileName())
            os.unlink(self.raw_nifti.minfFileName())
        context.runProcess(conv, self.raw, self.raw_nifti)
        # launchFreesurferCommand(context, '',
                                #'mri_convert',
                                # self.raw.fullPath(),
                                # self.raw_nifti.fullPath())
        self.raw_nifti._minfAttributes = {}
        self.raw_nifti.saveMinf()
        context.system(os.path.basename(sys.executable),
                       '-c',
                       'from freesurfer.setAnatTransformation import setAnatTransformation as f; f(\"%s\");' % (self.raw_nifti.fullPath()))
        self.raw_nifti.readAndUpdateMinf()
        if self.referential:
            self.raw_nifti.setMinf(
                'referential', self.referential.uuid(), saveMinf=True)
            registration.getTransformationManager(
            ).copyReferential(self.referential,
                              self.raw_nifti)

    # reset minf attributes in case there was an existing older diskitem
    if os.path.exists(self.orig_nifti.minfFileName()):
        context.write('removing residual .minf file %s' %
                      self.orig_nifti.minfFileName())
        os.unlink(self.orig_nifti.minfFileName())
    if os.path.exists(self.nu_nifti.minfFileName()):
        context.write('removing residual .minf file %s' %
                      self.nu_nifti.minfFileName())
        os.unlink(self.nu_nifti.minfFileName())
    if os.path.exists(self.ribbon_nifti.minfFileName()):
        context.write('removing residual .minf file %s' %
                      self.ribbon_nifti.minfFileName())
        os.unlink(self.ribbon_nifti.minfFileName())
    if os.path.exists(self.aseg_nifti.minfFileName()):
        context.write('removing residual .minf file %s' %
                      self.aseg_nifti.minfFileName())
        os.unlink(self.aseg_nifti.minfFileName())
    if os.path.exists(self.aparc_aseg_nifti.minfFileName()):
        context.write('removing residual .minf file %s' %
                      self.aparc_aseg_nifti.minfFileName())
        os.unlink(self.aparc_aseg_nifti.minfFileName())
    if os.path.exists(self.aparc_a2009s_aseg_nifti.minfFileName()):
        context.write('removing residual .minf file %s' %
                      self.aparc_a2009s_aseg_nifti.minfFileName())
        os.unlink(self.aparc_a2009s_aseg_nifti.minfFileName())

    # convert images
    context.runProcess(conv, self.orig, self.orig_nifti)
    context.runProcess(conv, self.nu, self.nu_nifti)
    context.runProcess(conv, self.ribbon, self.ribbon_nifti)
    context.runProcess(conv, self.aseg, self.aseg_nifti)
    context.runProcess(conv, self.aparc_aseg, self.aparc_aseg_nifti)
    context.runProcess(
        conv, self.aparc_a2009s_aseg, self.aparc_a2009s_aseg_nifti)
    # launchFreesurferCommand( context, '',
                            #'mri_convert',
                            # self.RawImage.fullPath(),
                            # self.NiiRawImage.fullPath() )
    # launchFreesurferCommand( context, '',
                            #'mri_convert',
                            # self.NuImage.fullPath(),
                            # self.NiiNuImage.fullPath() )
    # launchFreesurferCommand( context, '',
                            #'mri_convert',
                            # self.RibbonImage.fullPath(),
                            # self.NiiRibbonImage.fullPath() )

    # set minf files
    self.orig_nifti._minfAttributes = {}
    self.orig_nifti.saveMinf()
    self.nu_nifti._minfAttributes = {}
    self.nu_nifti.saveMinf()
    self.ribbon_nifti._minfAttributes = {}
    self.ribbon_nifti.saveMinf()
    self.aseg_nifti._minfAttributes = {}
    self.aseg_nifti.saveMinf()
    self.aparc_aseg_nifti._minfAttributes = {}
    self.aparc_aseg_nifti.saveMinf()
    self.aparc_a2009s_aseg_nifti._minfAttributes = {}
    self.aparc_a2009s_aseg_nifti.saveMinf()
    context.pythonSystem('-c',
                         'from freesurfer.setAnatTransformation import setAnatTransformation as f; f(\"%s\");' % (self.orig_nifti.fullPath()))
    context.pythonSystem('-c',
                         'from freesurfer.setAnatTransformation import setAnatTransformation as f; f(\"%s\");' % (self.nu_nifti.fullPath()))
    context.pythonSystem('-c',
                         'from freesurfer.setAnatTransformation import setAnatTransformation as f; f(\"%s\");' % (self.ribbon_nifti.fullPath()))
    context.pythonSystem('-c',
                         'from freesurfer.setAnatTransformation import setAnatTransformation as f; f(\"%s\");' % (self.aseg_nifti.fullPath()))
    context.pythonSystem('-c',
                         'from freesurfer.setAnatTransformation import setAnatTransformation as f; f(\"%s\");' % (self.aparc_aseg_nifti.fullPath()))
    context.pythonSystem('-c',
                         'from freesurfer.setAnatTransformation import setAnatTransformation as f; f(\"%s\");' % (self.aparc_a2009s_aseg_nifti.fullPath()))
    self.orig_nifti.readAndUpdateMinf()
    self.nu_nifti.readAndUpdateMinf()
    self.ribbon_nifti.readAndUpdateMinf()
    self.aseg_nifti.readAndUpdateMinf()
    self.aparc_aseg_nifti.readAndUpdateMinf()
    self.aparc_a2009s_aseg_nifti.readAndUpdateMinf()

    # referential
    if self.referential:
        self.orig_nifti.setMinf('referential',
                                self.referential.uuid(),
                                saveMinf=True)
        self.nu_nifti.setMinf('referential',
                              self.referential.uuid(),
                              saveMinf=True)
        self.ribbon_nifti.setMinf('referential',
                                  self.referential.uuid(),
                                  saveMinf=True)
        self.aseg_nifti.setMinf('referential',
                                self.referential.uuid(),
                                saveMinf=True)
        self.aparc_aseg_nifti.setMinf('referential',
                                      self.referential.uuid(),
                                      saveMinf=True)
        self.aparc_a2009s_aseg_nifti.setMinf('referential',
                                             self.referential.uuid(),
                                             saveMinf=True)
        registration.getTransformationManager().copyReferential(
            self.referential, self.orig_nifti)
        registration.getTransformationManager().copyReferential(
            self.referential, self.nu_nifti)
        registration.getTransformationManager().copyReferential(
            self.referential, self.ribbon_nifti)
        registration.getTransformationManager().copyReferential(
            self.referential, self.aseg_nifti)
        registration.getTransformationManager().copyReferential(
            self.referential, self.aparc_aseg_nifti)
        registration.getTransformationManager().copyReferential(
            self.referential, self.aparc_a2009s_aseg_nifti)
