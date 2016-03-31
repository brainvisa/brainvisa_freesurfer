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
import argparse
import textwrap

# soma module
import soma.aims.texturetools as satt


#----------------------------Functions-----------------------------------------


def mylist(string):
    return json.loads(string)


def parse_args(argv):
    """Parses the given list of arguments."""

    # creating a parser
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""\
            -------------------------------------------------------------------
            Create the average gyri texture (.tex and .gii).
            usage : python average_texture.py output subject1 ... subjectN'
            -------------------------------------------------------------------
            """))

    # adding arguments
    parser.add_argument(
        "inputs", type=mylist, help="list of gryi segmentations")
    parser.add_argument("output", type=str, help="averaged gyri segmentation")

    # parsing arguments
    return parser, parser.parse_args(argv)


#----------------------------Main program--------------------------------------


def main():
    # load the arguments of parser (delete script name: sys.arg[0])
    print json.dumps(eval(sys.argv[1]))
    arguments = (json.dumps(eval(sys.argv[1])), sys.argv[2])
    parser, args = parse_args(arguments)

    # create and write the average gyri segmentation
    satt.average_texture(args.otex, args.itex)

if __name__ == "__main__":
    main()
