#!/usr/bin/env python
###############################################################################
# This software and supporting documentation are distributed by CEA/NeuroSpin,
# Batiment 145, 91191 Gif-sur-Yvette cedex, France. This software is governed
# by the CeCILL license version 2 under French law and abiding by the rules of
# distribution of free software. You can  use, modify and/or redistribute the
# software under the terms of the CeCILL license version 2 as circulated by
# CEA, CNRS and INRIA at the following URL "http://www.cecill.info".
###############################################################################


#----------------------------Imports-------------------------------------------


# python system module
import sys
import json
import numpy
import argparse
import textwrap

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
            usage : python average_mesh.py output subject1 ... subjectN'
            -------------------------------------------------------------------
            """))

    # adding arguments
    parser.add_argument("inputs", type=mylist, help="list of individual mesh")
    parser.add_argument("output", type=str, help="averaged mesh")

    # parsing arguments
    return parser, parser.parse_args(argv)


#----------------------------Function------------------------------------------


def average_mesh(avg_mesh, list_filenames):
    """Create an average mesh from a list of meshes.
    """
    list_mesh = []
    for filename in list_filenames:
        m = aims.read(filename)
        list_mesh.append(numpy.array(m.vertex()))
    
    lmesh = numpy.array(list_mesh)
    nb_mesh = aims.read(list_filenames[0])
    
    for i in range(len(nb_mesh.vertex())):
        nb_mesh.vertex()[i] = numpy.mean(lmesh[:, i], 0)
    
    nb_mesh.updateNormals()
    aims.write(nb_mesh, avg_mesh)


#----------------------------Main program--------------------------------------


def main():
    # load the arguments of parser (delete script name: sys.arg[0])
    arguments = (json.dumps(eval(sys.argv[1])), sys.argv[2])
    parser, args = parse_args(arguments)

    # create and write the average gyri segmentation
    average_mesh(args.output, args.inputs)


if __name__ == "__main__":
    main()
