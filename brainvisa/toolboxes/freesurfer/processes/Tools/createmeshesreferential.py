from __future__ import absolute_import
from brainvisa.processes import *
from brainvisa import registration
from brainvisa.tools import aimsGlobals

name = 'Create FreeSurfer Meshes referential'

signature = Signature(
    'anat', ReadDiskItem('RawFreeSurferAnat', 'aims readable volume formats'),
  'meshes_referential', WriteDiskItem('Referential of Pial', 'Referential'),
)


def initialization(self):
    self.linkParameters('meshes_referential', 'anat')


def execution(self, context):
    tm = registration.getTransformationManager()
    ref = tm.findOrCreateReferential(diskItem=self.anat,
                                     referentialType='Referential of Pial',
                                     assign=False, output_diskitem=self.meshes_referential)
    self.meshes_referential.setMinf('direct_referential', 1, saveMinf=True)
    # warning writes anat header, which may be read-only
    refs = aimsGlobals.aimsVolumeAttributes(self.anat)['referentials']
    refs[-1] = self.meshes_referential.uuid()
    self.anat.setMinf('referentials', refs, saveMinf=True)
