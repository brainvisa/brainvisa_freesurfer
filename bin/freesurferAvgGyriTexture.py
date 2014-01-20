#!/usr/bin/env python
import optparse
import sys
import soma.aims.texturetools as satt

def parseOpts( argv ):
  description = 'Create average gyri texture. usage : python average_texture.py output.gii(.tex) subject1.gii(.tex) ... subjectN.gii(.tex)'
  parser = optparse.OptionParser( description )
  parser.add_option('-i', '--itex', dest = 'itex',
    metavar = 'FILE', action='append',
    help = 'inputs texture (list of)' )
  parser.add_option('-o', '--otex', dest = 'otex',
    metavar = 'FILE',
    help = 'output texture' )
  return parser, parser.parse_args( argv )

def main():
  parser, ( options, args ) = parseOpts( sys.argv )
  satt.average_texture( options.otex, options.itex )

if __name__ == "__main__" : main()