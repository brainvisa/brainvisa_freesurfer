from numpy import array
from tio import Texture
import sys

def usage():
    print "concatenate textures"
    print "usage: python concatenate_textures.py output.tex file1.tex ... fileN.tex"

def concatenate_textures(output, files):
    print 'output', output, "nb_files", len(files)
    print files
    data = []
    for i in files:
        print i
        t = Texture.read(i)
        data.append(t.data.squeeze())

    data = array(data).flatten()
    t = Texture(filename=output, data=data)
    t.write()

if __name__ == "__main__":
    if len(sys.argv)<=3:
        usage()
        sys.exit(1)
    output = sys.argv[1]
    files = sys.argv[2:]
    concatenate_textures(output, files)
