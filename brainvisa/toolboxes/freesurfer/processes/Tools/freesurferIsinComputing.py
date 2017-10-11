import os, sys
from brainvisa.processes import *

name = 'Computation of resampling parameters'
userlevel = 2

signature = Signature(
    'SphereRegMesh', ReadDiskItem('SphereReg', 'Aims Mesh formats'),
    'icosphere_type', Choice('brainvisa', 'hcp'),
    'destination', ReadDiskItem('Ico Mesh', 'GIFTI File'),
    'Isin', WriteDiskItem('BaseFreesurferType', 'FreesurferIsin'),
)

def initialization(self):
    def link_sphere(self, dummy):
        atts = {}
        if self.SphereRegMesh is not None:
            atts.update(self.SphereRegMesh.hierarchyAttributes())
        if self.icosphere_type:
            # if icosphere_type is specified, use it for selection
            atts['icosphere_type'] = self.icosphere_type
            if self.icosphere_type != 'hcp' and 'side' in atts:
                # only the HCP mesh has side information, otherwise drop it
                del atts['side']
        return self.signature['destination'].findValue(atts)

    self.linkParameters('Isin', 'SphereRegMesh')
    self.linkParameters('destination', ('SphereRegMesh', 'icosphere_type'),
                        link_sphere)
    self.setOptional('icosphere_type')

  
def execution(self, context):
    context.write('Compute \'isin\' file, allowing the mesh resampling.')

    context.write('%s -c \"from freesurfer.regularizeSphericalMesh_hack4 import regularizeSphericalMesh as f; f(\'%s\', \'%s\', \'%s\');\"'
                  %(os.path.basename(sys.executable),
                    self.SphereRegMesh.fullPath(), self.Isin.fullPath(),
                    self.destination.fullPath()))

    context.pythonSystem(
        '-c',
        'from freesurfer.regularizeSphericalMesh_hack4 import regularizeSphericalMesh as f; f(\"%s\", \"%s\", \"%s\"); '
        %(self.SphereRegMesh.fullPath(), self.Isin.fullPath(),
          self.destination.fullPath()))


