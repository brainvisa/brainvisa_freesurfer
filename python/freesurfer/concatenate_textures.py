from numpy import array
import numpy
#from tio import Texture
from soma import aims
import sys

def usage():
  print "concatenate textures"
  #print "usage: python concatenate_textures.py output.tex file1.tex ... fileN.tex"

def concatenate_textures(output, fileL, fileR): 
  gyriTexR = aims.read(fileR)
  gyriTexL = aims.read(fileL)
  gyriTexB = aims.TimeTexture_S16()
  vertexNbR = gyriTexR[0].nItem()
  vertexNbL = gyriTexL[0].nItem()
  vertexNbB = vertexNbR + vertexNbL
  gyriTexB[0].reserve(vertexNbB)
  for v in xrange(vertexNbL):
    gyriTexB[0].push_back(gyriTexL[0][v] + 1)
    lh_max = gyriTexB[0].arraydata().max()
  gyriTexB[0].arraydata()[gyriTexB[0].arraydata() == 0] = 1
  for v in xrange(vertexNbR):
    value = gyriTexR[0][v] + 1 + lh_max
    if value == lh_max:
      value = value + 1
    gyriTexB[0].push_back(value)
  aims.write(gyriTexB, output)

if __name__ == "__main__":
  if len(sys.argv)<=3:
    usage()
    sys.exit(1)
  output = sys.argv[1]
  fileL = sys.argv[2]
  fileR = sus.argv[3]
  concatenate_textures(output, fileL, fileR)

