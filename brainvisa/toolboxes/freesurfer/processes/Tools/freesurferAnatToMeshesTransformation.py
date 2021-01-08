from __future__ import absolute_import
from brainvisa.processes import *
from brainvisa.tools import aimsGlobals
from brainvisa import registration
from soma import aims

name = 'Anat To FreeSurfer Meshes Transformation'

signature = Signature(
    'anat', ReadDiskItem('RawFreeSurferAnat', 'Aims readable volume formats'),
    'freesurfer_meshes_referential',
        ReadDiskItem('Referential of Pial', 'Referential'),
    'anat_referential',
        ReadDiskItem('Referential of Raw T1 MRI', 'Referential'),
    'scanner_based_to_mni',
      ReadDiskItem('Freesurfer Scanner To MNI Transformation',
                   'Transformation matrix'),
    'fs_mesh', ReadDiskItem('White', 'aims mesh formats'),
    'anat_to_meshes_transform',
        WriteDiskItem('Freesurfer Anat To Meshes Transformation',
                      'Transformation matrix'),
)


def initialization(self):
    self.linkParameters('anat_referential', 'anat')
    self.linkParameters('freesurfer_meshes_referential', 'anat')
    self.linkParameters('anat_to_meshes_transform',
                        'freesurfer_meshes_referential')


def execution(self, context):
    atts = aimsGlobals.aimsVolumeAttributes(self.anat)
    sb = list(atts.get('referentials', [])).index(
        'Scanner-based anatomical coordinates')
    if sb < 0:
        raise ValueError('no scanner-based transformation in anat image')
    a2sb = aims.AffineTransformation3d(atts['transformations'][sb])
    sb2mni = aims.read(self.scanner_based_to_mni.fullPath())
    mesh = aims.read(self.fs_mesh.fullPath())
    mrefs = list(mesh.header().get('referentials', []))
    mref = -1
    for r in ('Talairach', aims.StandardReferentials.mniTemplateReferential(),
              aims.StandardReferentials.mniTemplateReferentialID()):
        mref = mrefs.index('Talairach')
        if mref >= 0:
            break
    if mref < 0:
        raise ValueError('no Talairach/MNI transformation in mesh')
    m2mni = aims.AffineTransformation3d(mesh.header()['transformations'][mref])

    tr = m2mni.inverse() * sb2mni * a2sb

    aims.write(tr, self.anat_to_meshes_transform.fullPath())
    self.anat_to_meshes_transform.setMinf('source_referential',
                                          self.anat_referential.uuid(),
                                          saveMinf=False)
    self.anat_to_meshes_transform.setMinf(
        'destination_referential', self.freesurfer_meshes_referential.uuid(),
        saveMinf=True)
    tm = registration.getTransformationManager()
    tm.setNewTransformationInfo(
        self.anat_to_meshes_transform,
        source_referential=self.anat_referential,
        destination_referential=self.freesurfer_meshes_referential)
