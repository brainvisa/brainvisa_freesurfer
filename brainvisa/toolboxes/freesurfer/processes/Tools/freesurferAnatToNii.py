# -*- coding: utf-8 -*-
import os
import sys
from brainvisa.processes import *
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand
from brainvisa import registration

name = "Convert Freesurfer images to Nifti format"
userLevel = 2

signature = Signature(
    'AnatImage', ReadDiskItem(
        'RawFreesurferAnat',
        'FreesurferMGZ',
        enableConversion=False),
  'NiiAnatImage', WriteDiskItem(
      'RawFreesurferAnat',
      ['gz compressed NIFTI-1 image', 'NIFTI-1 image']),
  'NuImage', ReadDiskItem(
      'Nu FreesurferAnat',
      'FreesurferMGZ',
      enableConversion=False),
  'NiiNuImage', WriteDiskItem(
      'Nu FreesurferAnat',
      ['gz compressed NIFTI-1 image', 'NIFTI-1 image']),
  'RibbonImage', ReadDiskItem(
      'Ribbon Freesurfer',
      'FreesurferMGZ',
      enableConversion=False),
  'NiiRibbonImage', WriteDiskItem(
      'Ribbon Freesurfer',
      ['gz compressed NIFTI-1 image', 'NIFTI-1 image']),
  'referential', ReadDiskItem(
      'Referential of Raw T1 MRI',
      'Referential'),
)


def initialization(self):
    self.linkParameters('NiiAnatImage', 'AnatImage')
    self.linkParameters('NuImage', 'AnatImage')
    self.linkParameters('NiiNuImage', 'NuImage')
    self.linkParameters('RibbonImage', 'AnatImage')
    self.linkParameters('NiiRibbonImage', 'RibbonImage')
    self.linkParameters('referential', 'AnatImage')
    self.setOptional('referential')


def execution(self, context):

    if os.path.exists(self.NiiAnatImage.minfFileName()):
        context.write('removing residual .minf file %s' %
                      self.NiiAnatImage.minfFileName())
        os.unlink(self.NiiAnatImage.minfFileName())
    if os.path.exists(self.NiiNuImage.minfFileName()):
        context.write('removing residual .minf file %s' %
                      self.NiiNuImage.minfFileName())
        os.unlink(self.NiiNuImage.minfFileName())
    if os.path.exists(self.NiiRibbonImage.minfFileName()):
        context.write('removing residual .minf file %s' %
                      self.NiiRibbonImage.minfFileName())
        os.unlink(self.NiiRibbonImage.minfFileName())

    # convert from .mgz to .nii with Freesurfer
    launchFreesurferCommand(context, '',
                            'mri_convert',
                            self.AnatImage.fullPath(),
                            self.NiiAnatImage.fullPath())
    launchFreesurferCommand(context, '',
                            'mri_convert',
                            self.NuImage.fullPath(),
                            self.NiiNuImage.fullPath())
    launchFreesurferCommand(context, '',
                            'mri_convert',
                            self.RibbonImage.fullPath(),
                            self.NiiRibbonImage.fullPath())

    # reset minf attributes in case there was an existing older diskitem
    self.NiiAnatImage._minfAttributes = {}
    self.NiiNuImage._minfAttributes = {}
    self.NiiRibbonImage._minfAttributes = {}
    self.NiiAnatImage.saveMinf()
    self.NiiNuImage.saveMinf()
    self.NiiRibbonImage.saveMinf()

    # referential
    if self.referential is not None:
        self.NiiAnatImage.setMinf('referential', self.referential.uuid(),
                                  saveMinf=True)
        registration.getTransformationManager().copyReferential(
            self.referential, self.NiiAnatImage)
    # Nu and ribbon are in a different referential as Anat. For now we
    # don't set it. Their scanner-based transform should help to make the link.
