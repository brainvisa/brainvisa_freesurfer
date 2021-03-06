from __future__ import absolute_import
import os
import sys
from brainvisa.processes import *

name = 'Computation of resampling parameters'
userlevel = 2

signature = Signature(
    'SphereRegMesh', ReadDiskItem('SphereReg', 'Aims Mesh formats'),
    'icosphere_type', Choice('brainvisa 40k', 'hcp 32k', 'freesurfer ic7 163k',
                             'freesurfer ic6 40k', 'freesurfer ic5 10k'),
    'destination', ReadDiskItem('Ico Mesh', 'Aims mesh formats'),
    'Isin', WriteDiskItem('BaseFreesurferType', 'FreesurferIsin'),
)


def initialization(self):
    def link_sphere(self, dummy):
        atts = {}
        if self.SphereRegMesh is not None:
            atts.update({k: v
                         for k, v in
                            self.SphereRegMesh.hierarchyAttributes().items()
                         if k in ('side', )})
        if self.icosphere_type:
            # if icosphere_type is specified, use it for selection
            atts['icosphere_type'] = self.icosphere_type
            if not self.icosphere_type.startswith('hcp') and 'side' in atts:
                # only the HCP mesh has side information, otherwise drop it
                del atts['side']
        print('link_sphere atts:', atts)
        return self.signature['destination'].findValue(atts)

    self.linkParameters('Isin', 'SphereRegMesh')
    self.linkParameters('destination', ('SphereRegMesh', 'icosphere_type'),
                        link_sphere)
    self.setOptional('icosphere_type')


def execution(self, context):
    context.write('Compute \'isin\' file, allowing the mesh resampling.')

    context.write('%s -c \"from freesurfer.regularizeSphericalMesh_hack4 import regularizeSphericalMesh as f; f(\'%s\', \'%s\', \'%s\');\"'
                  % (os.path.basename(sys.executable),
                     self.SphereRegMesh.fullPath(), self.Isin.fullPath(),
                     self.destination.fullPath()))

    context.pythonSystem(
        '-c',
        'from freesurfer.regularizeSphericalMesh_hack4 import regularizeSphericalMesh as f; f(\"%s\", \"%s\", \"%s\"); '
        % (self.SphereRegMesh.fullPath(), self.Isin.fullPath(),
           self.destination.fullPath()))
