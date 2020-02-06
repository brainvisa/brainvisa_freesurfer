#!/usr/bin/env python
#
# This software and supporting documentation are distributed by CEA/NeuroSpin,
# Batiment 145, 91191 Gif-sur-Yvette cedex, France. This software is governed
# by the CeCILL license version 2 under French law and abiding by the rules of
# distribution of free software. You can  use, modify and/or redistribute the
# software under the terms of the CeCILL license version 2 as circulated by
# CEA, CNRS and INRIA at the following URL "http://www.cecill.info".
#


#----------------------------Imports-------------------------------------------


# python system module
import sys
import json
import numpy
import argparse
import textwrap
import os

# soma-base module
from soma import aims


#----------------------------Header--------------------------------------------


def mylist(string):
    return json.loads(string)


def parse_args(argv):
    """Parses the given list of arguments."""

    # creating a parser
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""\
            -------------------------------------------------------------------
            Create an average mesh from resampled brain mesh.
            usage : python %s output subject1 ... subjectN'
            All meshes should have vertex-by-vertex correspondance.
            Transformations can be applied to get all of them in a common space.
            -------------------------------------------------------------------
            """ % os.path.basename(sys.argv[0])))

    # adding arguments
    parser.add_argument(
        "inputs", type=mylist,
        help="list of individual mesh, json format, ex '[\"bobo.gii\", "
        "\"bubu.gii\"]'")
    parser.add_argument("output", type=str, help="averaged mesh")
    parser.add_argument(
        '--transforms', type=mylist,
        help='list of individual transforms to get each mesh '
        'to a common referential (json format). A transform may be either:\n'
        '* a transformation file (.trm)\n'
        '* a mesh or volume filename + referential info:\n'
        '  "totor.gii:Talairach"\n'
        '  will load totor.gii, then look in its header if it has a transform '
        '  to referential "Talairach".'
        '  mesh should have a transform to the referential of mesh '
        '  "totor.gii", they will be combined.'
        '* a transform in the mesh header, if trans_filename is None and '
        '  referential is a referential ID found in the header.')
    parser.add_argument('-f', '--final_transform', type=str, default=None,
                        help='final transformation to apply to the average '
                        'mesh')
    parser.add_argument('-r', '--referential', type=str, default=None,
                        help='target referential to get transform to in the '
                        'current mesh header')

    # parsing arguments
    return parser, parser.parse_args(argv)


#----------------------------Function------------------------------------------


def average_mesh(avg_mesh, list_filenames, transform_list=[],
                 final_transform=None, referential=None):
    """Create an average mesh from a list of meshes.

    Parameters
    ----------
    avg_mesh: str
        output filename for the average mesh
    list_filenames: list of str
        meshes filenames to be averaged
    transform_list: list of str (optional)
        transformations to be applied to each mesh. If specified, the list size
        should match the size of list_filenames.
        Items can be:
        * a transformation file (.trm)
        * a mesh or volume filename + referential info:
          "totor.gii:Talairach"
          will load totor.gii, then look in its header if it has a transform to
          referential "Talairach".
          mesh should have a transform to the referential of mesh "totor.gii",
          they will be combined.
    final_transform: str (optional)
        transformation filename (.trm). This transformation is applied after
        averaging to get the mesh to a given coordinates system.
    referential: str (optional)
        Specifies that transformations to be applied to each mesh should be
        found in the meshes headers, and that they should go to this specific
        referential. Only used when transform_list is not provided.
    """
    list_mesh = []
    warned = False
    if not transform_list:
        transform_list = [None] * len(list_filenames)
    ref = None
    nb_mesh = None
    direct_tr = True
    for filename, trans_filename in zip(list_filenames, transform_list):
        m = aims.read(filename)
        if nb_mesh is None:
            nb_mesh = m
        tr_def = get_transform(m, trans_filename, referential)
        if tr_def is not None:
            tr, ref_name = tr_def
            aims.SurfaceManip.meshTransform(m, tr)
            if not tr.isDirect():
                direct_tr = False
            if ref is None and ref_name is not None:
                ref = ref_name
        elif not warned:
            warned = True
            print('Warning: transform not provided, the average mesh will be '
                  'inaccurate.')
        list_mesh.append(numpy.array(m.vertex()))

    lmesh = numpy.array(list_mesh)

    for i in range(len(nb_mesh.vertex())):
        nb_mesh.vertex()[i] = numpy.mean(lmesh[:, i], 0)

    nb_mesh.updateNormals()
    if final_transform is not None:
        f_trans = aims.read(final_transform)
        aims.SurfaceManip.meshTransform(nb_mesh, f_trans)
        if not f_trans.isDirect():
            direct_tr = not direct_tr
        if 'destination_referential' in f_trans.header():
            ref = f_trans.header()['destination_referential']
        else:
            ref = None
    if ref is not None:
        nb_mesh.header()['referential'] = ref

    mat = None
    old_ff = 'clockwise'
    # if 'material' in nb_mesh.header():
    if nb_mesh.header().has_key('material'):
        mat = nb_mesh.header()['material']
        if 'front_face' in mat:
            old_ff = mat['front_face']
    if not direct_tr:
        if old_ff == 'clockwise':
            ff = 'counterclockwise'
        else:
            ff = 'clockwise'
        if not mat:
            mat = {}
            nb_mesh.header()['material'] = mat
        mat['front_face'] = ff
    if nb_mesh.header().has_key('transformations'):
        del nb_mesh.header()['transformations']
        del nb_mesh.header()['referentials']

    aims.write(nb_mesh, avg_mesh)


def get_transform(mesh, trans_filename, referential=None):
    """Get transformation from file/header description.
    trans_filename may be:
    * a transformation file (.trm)
    * a mesh or volume filename + referential info:
      "totor.gii:Talairach"
      will load totor.gii, then look in its header if it has a transform to
      referential "Talairach".
      mesh should have a transform to the referential of mesh "totor.gii", they
      will be combined.
    * a transform in the mesh header, if trans_filename is None and referential
      is a referential ID found in the header.

    Returns
    -------
    trans, ref: aims.AffineTransformation3d, str
        if trans can be found, or None otherwise. ref it the target referential
        name
    """
    if not trans_filename:
        if referential is not None and mesh.header().has_key('referentials') \
                and referential in mesh.header()['referentials']:
            for iref, ref in enumerate(mesh.header()['referentials']):
                if ref == referential:
                    break
            tr = aims.AffineTransformation3d(
                mesh.header()['transformations'][iref])
            return tr, referential
        return None
    if ':' not in trans_filename:
        # .trm case
        tr = aims.read(trans_filename)
        ref_name = None
        if 'destination_referential' in tr.header():
            ref_name = tr.header()['destination_referential']
        return tr, ref_name
    else:
        # mesh (or other object):
        obj_file, ref_name = trans_filename.split(':')
        obj = aims.read(obj_file)
        h = obj.header()
        oref = h['referential']
        mrefs = mesh.header()['referentials']
        if oref not in mrefs:
            print('intermediate referential', oref, 'not in mesh header')
            return None
        if ref_name not in h['referentials']:
            print('target referential', ref_name, 'not in target mesh header')
        for i, r in enumerate(mrefs):
            if r == oref:
                tnum = i
                break
        mtrans = aims.AffineTransformation3d(
            mesh.header()['transformations'][tnum])
        for i, r in enumerate(h['referentials']):
            if r == ref_name:
                tnum = i
                break
        ttrans = aims.AffineTransformation3d(h['transformations'][tnum])
        return ttrans * mtrans, ref_name


#----------------------------Main program--------------------------------------


def main():
    # load the arguments of parser (delete script name: sys.arg[0])
    # arguments = (json.dumps(eval(sys.argv[1])), sys.argv[2])
    # parser, args = parse_args(arguments)
    parser, args = parse_args(sys.argv[1:])

    # create and write the average gyri segmentation
    average_mesh(args.output, args.inputs, args.transforms,
                 args.final_transform, args.referential)


if __name__ == "__main__":
    main()
