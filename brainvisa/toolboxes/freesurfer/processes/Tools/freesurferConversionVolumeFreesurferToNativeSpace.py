# -*- coding: utf-8 -*-

from __future__ import print_function

from brainvisa.processes import *
from brainvisa import registration
from soma import aims


name = "Conversion of Freesurfer images to original t1mri space"
userLevel = 2


signature = Signature(
    'image', ReadDiskItem(
        #'3D Volume',
        'Label Volume',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image']),
    'orig_t1mri', ReadDiskItem(
        'RawFreesurferAnat',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image']),
    'image_in_native_space', WriteDiskItem(
        #'3D Volume',
        'Label Volume',
        ['gz compressed NIFTI-1 image', 'NIFTI-1 image']),
)


def initialization(self):
    def linkOutput(proc, dummy):
        if self.image is not None:
            basepath = self.image.fullPath()[:self.image.fullPath().find('.')]
            ext = self.image.fullPath()[self.image.fullPath().find('.'):]
            output = basepath + '_native' + ext
            return output
    
    self.linkParameters('orig_t1mri', 'image')
    self.linkParameters('image_in_native_space', 'image', linkOutput)


def execution(self, context):
    # read input images
    img = aims.read(self.image.fullPath())
    orig = aims.read(self.orig_t1mri.fullPath())
    
    # transformations recuperation
    s2sb = aims.AffineTransformation3d(img.header()['transformations'][0])
    n2sb = aims.AffineTransformation3d(orig.header()['transformations'][0])
    s2n = n2sb.inverse() * s2sb

    transfo_fs2nat = context.temporary('Transformation matrix')
    aims.write(s2n, transfo_fs2nat.fullPath())

    context.system('AimsApplyTransform',
                   '-i', self.image,
                   '-o', self.image_in_native_space,
                   '-m', transfo_fs2nat,
                   '-t', 0,
                   '-r', self.orig_t1mri)
    
    tm = registration.getTransformationManager()
    tm.copyReferential(self.orig_t1mri, self.image_in_native_space)

