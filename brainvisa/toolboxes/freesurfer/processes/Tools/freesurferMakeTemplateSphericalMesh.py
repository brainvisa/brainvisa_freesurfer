# -*- coding: utf-8 -*-
from brainvisa.processes import *
from brainvisa.group_utils import Subject
from soma.minf.api import registerClass, readMinf
from soma import aims, aimsalgo

name = 'Make template spherical mesh'
userlevel = 2

signature = Signature(
  'group', ReadDiskItem('Freesurfer Group definition', 'XML' ),
  'triangles_number', Integer(),
  'LeftTemplateMesh', WriteDiskItem('Ico Mesh', 'GIFTI File',
                                    requiredAttributes = {'side':'left'}),
  'RightTemplateMesh', WriteDiskItem('Ico Mesh', 'GIFTI File',
                                     requiredAttributes = {'side':'right'}),
  'initial_icosphere_triangles_number', Integer(),
  'undecimated_icosphere', WriteDiskItem( 'Ico Mesh', 'GIFTI File' ),
  'LeftDensityTexture', WriteDiskItem( 'Texture', 'GIFTI File' ),
  'RightDensityTexture', WriteDiskItem( 'Texture', 'GIFTI File' ),
)

def initialization(self):
  self.triangles_number = 40000
  self.initial_icosphere_triangles_number = 200000
  self.linkParameters( 'RightTemplateMesh', 'LeftTemplateMesh' )
  self.setOptional( 'LeftDensityTexture', 'RightDensityTexture',
    'undecimated_icosphere' )
  self.linkParameters('RightDensityTexture', 'LeftDensityTexture')


def execution( self, context ):
  registerClass('minf_2.0', Subject, 'Subject')
  groupOfSubjects = readMinf(self.group.fullPath())

  sides = ( 'left', 'right' )
  outtmeshes = ( self.LeftTemplateMesh, self.RightTemplateMesh )
  outdtex = ( self.LeftDensityTexture, self.RightDensityTexture )

  icopolynum = self.initial_icosphere_triangles_number
  undecimatedWritten = False

  for side, outmesh, outtex in zip( sides, outtmeshes, outdtex ):
    # get a full icosphere
    icosphere = aims.SurfaceGenerator.icosphere( [ 0, 0, 0 ], 100., icopolynum )
    if not undecimatedWritten and self.undecimated_icosphere is not None:
      aims.write( icosphere, self.undecimated_icosphere.fullPath() )
      undecimatedWritten = True
    context.write( 'using an initial icosphere of', len( icosphere.polygon() ),
      'polygons, ', len( icosphere.vertex() ), 'vertices.' )
    subjects = []
    rattrs = { 'side' : side }
    density = None # density sum texture
    for subject in groupOfSubjects:
      context.write( '* subject:', subject )
      ssphere = ReadDiskItem( 'SphereReg',
        'Aims mesh formats' ).findValue( subject.attributes(),
        requiredAttributes = rattrs )
      subjects.append( ssphere )
      # read individual spherical mesh
      mesh = aims.read( ssphere.fullPath() )
      # calculate mesh density on sphere
      context.write( 'calculating mesh density' )
      denstex = aims.SurfaceManip.meshDensity( mesh )
      context.write( 'mesh size:', mesh.vertex().size(), ', texture size:',
        denstex[0].size() )
      # interpolate mesh on the icosphere
      mi = aims.MeshInterpoler( mesh, icosphere )
      mi.project()
      # interpolate density texture and accumulate it
      rdenstex = mi.resampleTexture( denstex )
      context.write( 'interpolated texture size:',rdenstex[0].size() )
      if density is None:
        density = rdenstex
        # invert density to get mean distance
        density[0].arraydata()[:] = 1. / density[0].arraydata()
      else: # add inverses (mean distance, inversed)
        ar = density[0].arraydata()
        ar += 1. / rdenstex[0].arraydata()
    # invert mean (or sum, no matter) distance
    density[0].arraydata()[:] = 1. / density[0].arraydata()
    if outtex is not None:
      aims.write( density, outtex.fullPath() )

    # decimate icosphere according to density
    decimrate = 100. - self.triangles_number * 100. / icopolynum
    context.write( 'decimation rate:', decimrate, '%' )
    me = aimsalgo.Mesher()
    me.setDecimation( decimrate, 5., 5., -180. )
    me.decimate( icosphere, [], density )
    aims.write( icosphere, outmesh.fullPath() )

