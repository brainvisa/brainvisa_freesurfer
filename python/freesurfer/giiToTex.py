from soma import aims
import sys
from tio import Texture
import numpy as n

#def giiToTex(filename):
    #out = filename[:filename.rfind('gii')]+'tex'
    #g = gifti.loadImage(filename)
    #data = n.array(g.getArrays()[0].data)
    #print data.shape
    #t = Texture(filename=out, data=data.squeeze())
    #t.write()

# Brainvisa function
def giftiToTex(filename, output):
    g = aims.read(filename)
    t = Texture(filename=output, data=g[0].arraydata())
    t.write()

#def usage():
    #print "Convert gifti texture to aims tex-format"
    #print "usage: python giiToTex.py filename.gii"
    #print "Output will be filename.tex"

#if __name__ == "__main__":
    #if len(sys.argv)!=2:
        #usage()
        #sys.exit(1)
    #giiToTex(sys.argv[1])
