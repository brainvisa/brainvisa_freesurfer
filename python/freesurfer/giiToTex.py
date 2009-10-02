import gifti
import sys
from tio import Texture

def giiToTex(filename):
    out = filename[:filename.rfind('gii')]+'tex'
    g = gifti.loadImage(filename)
    t = Texture(filename=out, data=g.getArrays()[0].data)
    t.write()

# Brainvisa function
def giftiToTex(filename, output):
    g = gifti.loadImage(filename)
    t = Texture(filename=output, data=g.getArrays()[0].data)
    t.write()

def usage():
    print "Convert gifti texture to aims tex-format"
    print "usage: python giiToTex.py filename.gii"
    print "Output will be filename.tex"

if __name__ == "__main__":
    if len(sys.argv)!=2:
        usage()
        sys.exit(1)
    giiToTex(sys.argv[1])
