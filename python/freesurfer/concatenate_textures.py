from numpy import array
#from tio import Texture
from soma import aims
import sys

def usage():
    print "concatenate textures"
    #print "usage: python concatenate_textures.py output.tex file1.tex ... fileN.tex"

def concatenate_textures(output, fileG, fileD): 
    gyriTexR = aims.read(fileD)
    gyriTexL = aims.read(fileG)
    gyriTexB = aims.TimeTexture_S16()
    vertexNbR = gyriTexR[0].nItem()
    vertexNbL = gyriTexL[0].nItem()
    vertexNbB = vertexNbR + vertexNbL
    gyriTexB[0].reserve(vertexNbB)
    for v in xrange(vertexNbL):
       gyriTexB[0].push_back(gyriTexL[0][v]+1)
       lh_max = gyriTexB[0].arraydata().max()
    for v in xrange(vertexNbR):
       gyriTexB[0].push_back(gyriTexR[0][v]+1 + lh_max)
    aims.write(gyriTexB, output)

if __name__ == "__main__":
    if len(sys.argv)<=3:
        usage()
        sys.exit(1)
    output = sys.argv[1]
    fileG = sys.argv[2]
    fileD = sus.argv[3]
    concatenate_textures(output, fileG, fileD)

