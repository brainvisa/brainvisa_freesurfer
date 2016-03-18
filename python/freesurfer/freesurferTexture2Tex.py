#! /usr/bin/env python2
from numpy import array, zeros
from soma import aims
import glob
from tio import Texture
import sys

def freesurferTexture2Tex(freesurferTexturesPath, brain_mesh, output_texture):
    mesh = aims.read(brain_mesh)
    nbv = len(mesh.vertex())
    data = zeros(nbv)
    data.fill(-1)

    for i in glob.glob(freesurferTexturesPath+"*"):
        value = int(i[i.rindex('-')+1:i.rindex('.')])
        f = open(i,'r')
        lines = f.readlines()
        for a in lines[2:]:
            data[int(a.split()[0])] = value
    
    tex = Texture(filename=output_texture,data=data)
    tex.write()

def freesurferTexture2TexBrainvisa(freesurferTextures, brain_mesh,
                                   output_texture):
    print 'freesurferTextures', freesurferTextures
    print 'brainmesh', brain_mesh
    print 'output texture', output_texture

    mesh = aims.read(brain_mesh)
    nbv = len(mesh.vertex())
    data = zeros(nbv)
    data.fill(-1)

    for i in freesurferTextures:
        value = int(i[i.rindex('-')+1:i.rindex('.')])
        f = open(i,'r')
        lines = f.readlines()
        for a in lines[2:]:
            data[int(a.split()[0])] = value
    
    tex = Texture(filename=output_texture,data=data)
    tex.write()

def usage():
    print "Convert freesurfer ASCII parcels file to aims tex file"
    print "usage : freesurferTexture2Tex.py freesurferTexturesPath brain_mesh output_texture"
    print ""
    print "Info: freesurferTexturesPath should be like /data/subject/label/lh.aparc.annot"
    print " and the prog will take into account all files begining with that."


if __name__ == "__main__":
    if len(sys.argv)!=4:
        usage()
        sys.exit(1)
    print "Freesurfer textures prototype: ", sys.argv[1]
    print "Brain mesh path:", sys.argv[2]
    print "Output texture path:", sys.argv[3]
    freesurferTexture2Tex(sys.argv[1], sys.argv[2], sys.argv[3])

