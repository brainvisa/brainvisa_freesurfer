
from __future__ import print_function
from __future__ import absolute_import
from soma import aims
import numpy as np
import os
from . import brainvisaFreesurfer as bvfs
import soma.subprocess
import sys
import tempfile
from soma.wip.application.api import Application


def write_asc(filename, mesh, tex):
    ''' Write mesh vertices + texture as Freesurfer .asc texture file

    Parameters
    ----------
    filename: str
        output .asc file name
    mesh: aims mesh
        mesh to write
    tex: aims texture or numpy array
        texture values to write
    '''
    v = mesh.vertex()
    if isinstance(tex, np.ndarray):
        t0 = tex
    else:
        t0 = tex[0].arraydata()
    with open(filename, 'w') as f:
        for l, x in enumerate(v):
            f.write('%03d %f %f %f %f\n' % (l, x[0], x[1], x[2], t0[l]))


def system(*args, **kwargs):
    ''' convenience function meant to replace context.system()
    '''
    return soma.subprocess.check_call(*args, **kwargs)


def resample_mesh_to_fs_ico(mesh, subject_dir, hemi, ico_order=6, context=None):
    ''' Resample a mesh to Freesurfer icosphere.

    mri_surf2surf is able to resample textures, but I could not find a way to
    actually resample meshes. So we convert each mesh coordinates array to a
    texture, use mri_surf2surf to resample it, then build a mesh with the
    structure of FS icosphere.

    Parameters
    ----------
    mesh: mesh to be resampled
    subject_dir: directory for the Freesurfer subject
    hemi: 'lh' or 'rh'
    ico_order: int
        ico order number used by Freesurfer (6=40962 vertices for instance)
    context: (optional)
        BrainVisa context

    Returns
    -------
    resampled mesh
    '''

    configuration = Application().configuration
    if context is None:
        # fake context using our system() which redirects to
        # soma.subprocess.check_call()
        context = sys.modules[__module__]

    v = np.asarray(mesh.vertex())
    filename = os.path.join(subject_dir, 'surf', hemi + '.x.asc')
    to_remove = [filename]
    write_asc(filename, mesh, v[:, 0])
    filename = os.path.join(subject_dir, 'surf', hemi + '.y.asc')
    to_remove.append(filename)
    write_asc(filename, mesh, v[:, 1])
    filename = os.path.join(subject_dir, 'surf', hemi + '.z.asc')
    to_remove.append(filename)
    write_asc(filename, mesh, v[:, 2])

    x_file_ = tempfile.mkstemp(suffix='x.gii')
    os.close(x_file_[0])
    x_file = x_file_[1]
    y_file_ = tempfile.mkstemp(suffix='y.gii')
    os.close(y_file_[0])
    y_file = y_file_[1]
    z_file_ = tempfile.mkstemp(suffix='z.gii')
    os.close(z_file_[0])
    z_file = z_file_[1]
    ico_file_ = tempfile.mkstemp(suffix='ico.gii')
    os.close(ico_file_[0])
    ico_file = ico_file_[1]
    del x_file_, y_file_, z_file_, ico_file_
    to_remove += [x_file, y_file, z_file, ico_file]

    try:
        cmd = ['mri_surf2surf', '--srcsubject', os.path.basename(subject_dir),
               '--trgsubject', 'ico', '--trgicoorder', str(ico_order),
               '--hemi', hemi, '--srcsurfval', 'x.asc', '--trgsurfval', x_file,
               '--src_type', 'curv']
        bvfs.launchFreesurferCommand(context, os.path.dirname(subject_dir),
                                     *cmd)

        cmd = ['mri_surf2surf', '--srcsubject', os.path.basename(subject_dir),
               '--trgsubject', 'ico', '--trgicoorder', str(ico_order),
               '--hemi', hemi, '--srcsurfval', 'y.asc', '--trgsurfval', y_file,
               '--src_type', 'curv']
        bvfs.launchFreesurferCommand(context, os.path.dirname(subject_dir),
                                     *cmd)

        cmd = ['mri_surf2surf', '--srcsubject', os.path.basename(subject_dir),
               '--trgsubject', 'ico', '--trgicoorder', str(ico_order),
               '--hemi', hemi, '--srcsurfval', 'z.asc', '--trgsurfval', z_file,
               '--src_type', 'curv']
        bvfs.launchFreesurferCommand(context, os.path.dirname(subject_dir),
                                     *cmd)

        ico_src = os.path.join(configuration.freesurfer.freesurfer_home_path,
                               'lib', 'bem', 'ic%d.tri' % ico_order)
        cmd = ['mris_convert', ico_src, ico_file]
        bvfs.launchFreesurferCommand(context, os.path.dirname(subject_dir),
                                     *cmd)

        resamp_x = aims.read(x_file)
        resamp_y = aims.read(y_file)
        resamp_z = aims.read(z_file)
        ico_mesh = aims.read(ico_file)

        new_vertex = np.hstack((np.expand_dims(resamp_x[0].arraydata(), 1),
                                np.expand_dims(resamp_y[0].arraydata(), 1),
                                np.expand_dims(resamp_z[0].arraydata(), 1)))
        ico_mesh.vertex().assign(new_vertex)
        return ico_mesh

    finally:
        for filename in to_remove:
            try:
                os.unlink(filename)
            except:
                pass
