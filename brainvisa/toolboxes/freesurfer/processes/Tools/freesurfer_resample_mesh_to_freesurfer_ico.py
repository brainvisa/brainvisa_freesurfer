
from brainvisa.processes import *
from soma import aims
from freesurfer import surf2surf_mesh as surf2surf

name = 'Resample mesh to Freesurfer Ico mesh'
userLevel = 2

signature = Signature(
    'mesh', ReadDiskItem('White Mesh', 'aims mesh formats'),
    'freesurfer_ico_order', Choice(0, 1, 2, 3, 4, 5, 6, 7),
    'resampled_mesh', WriteDiskItem('ResampledWhite', 'Aims mesh formats'),
)


def initialization(self):
    self.linkParameters('resampled_mesh', 'mesh')
    self.freesurfer_ico_order = 6


def execution(self, context):
    reload(surf2surf)
    mesh = aims.read(self.mesh.fullPath())
    subject_dir = os.path.dirname(os.path.dirname(self.mesh.fullPath()))
    if os.path.basename(self.mesh.fullPath()).startswith('lh.'):
        hemi = 'lh'
    else:
        hemi = 'rh'
    resampled_mesh = surf2surf.resample_mesh_to_fs_ico(
        mesh, subject_dir=subject_dir, hemi=hemi,
        ico_order=self.freesurfer_ico_order, context=context)
    aims.write(resampled_mesh, self.resampled_mesh.fullPath())

