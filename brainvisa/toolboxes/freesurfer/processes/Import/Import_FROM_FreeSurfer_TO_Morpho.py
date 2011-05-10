# -*- coding: utf-8 -*-
#  This software and supporting documentation are distributed by
#      Institut Federatif de Recherche 49
#      CEA/NeuroSpin, Batiment 145,
#      91191 Gif-sur-Yvette cedex
#      France
#
# This software is governed by the CeCILL license version 2 under
# French law and abiding by the rules of distribution of free software.
# You can  use, modify and/or redistribute the software under the 
# terms of the CeCILL license version 2 as circulated by CEA, CNRS
# and INRIA at the following URL "http://www.cecill.info". 
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or 
# data to be ensured and,  more generally, to use and operate it in the 
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license version 2 and that you accept its terms.
from neuroProcesses import *
from brainvisa import shelltools
import shfjGlobals, stat
from soma import aims
import numpy
import registration
from freesurfer.brainvisaFreesurfer import launchFreesurferCommand



name = 'Import From FreeSurfer to T1 pipeline'
roles = ('importer',)
userLevel = 2

def validation():
  try:
    from soma import aims
  except:
    raise ValidationError( 'aims module not available' )
  try:
    import numpy
  except:
    raise ValidationError( 'numpy module not available' )


signature=Signature(
  'T1_orig', ReadDiskItem( 'T1 FreesurferAnat',  'FreesurferMGZ' ),
  'nu_image', ReadDiskItem( 'Nu FreesurferAnat', 'FreesurferMGZ' ),
  'ribbon_image', ReadDiskItem( 'Ribbon Freesurfer', 'FreesurferMGZ' ),
  'Talairach_Auto', ReadDiskItem( 'Talairach Auto Freesurfer', 'MINC transformation matrix' ), 
 # 'normalized_referential', ReadDiskItem( 'Referential', 'Referential'),
  'T1_output', WriteDiskItem( 'Raw T1 MRI', [ 'GIS image', 'NIFTI-1 image', 'gz compressed NIFTI-1 image' ] ),
  'Biais_corrected_output', WriteDiskItem( 'T1 MRI Bias Corrected', [ 'GIS image', 'NIFTI-1 image', 'gz compressed NIFTI-1 image' ] ),
  'normalization_transformation',  WriteDiskItem( 'Transform Raw T1 MRI to Talairach-MNI template-SPM', 'Transformation matrix' ), 
  'Talairach_transform',  WriteDiskItem( 'Transform Raw T1 MRI to Talairach-AC/PC-Anatomist', 'Transformation matrix' ), 
  'histo_analysis', WriteDiskItem( 'Histo Analysis', 'Histo Analysis' ),
  #'hfiltered', WriteDiskItem( "T1 MRI Filtered For Histo", shfjGlobals.aimsWriteVolumeFormats ),
  #'white_ridges', WriteDiskItem( "T1 MRI White Matter Ridges",  shfjGlobals.aimsWriteVolumeFormats ),
  'Voronoi_output', WriteDiskItem( 'Voronoi Diagram', [ 'GIS image', 'NIFTI-1 image', 'gz compressed NIFTI-1 image' ] ),
  'Rgrey_white_output', WriteDiskItem( 'Right Grey White Mask', [ 'GIS image', 'NIFTI-1 image', 'gz compressed NIFTI-1 image' ] ),
  'Lgrey_white_output', WriteDiskItem( 'Left Grey White Mask', [ 'GIS image', 'NIFTI-1 image', 'gz compressed NIFTI-1 image' ] ),
  # 'input_spm_orientation', Choice( '0', '1', ), 
)


def initialization( self ):
  #self.signature[ 'output' ].browseUserLevel = 3
  #self.signature[ 'nu input' ].databaseUserLevel = 2
  self.linkParameters( 'nu_image', 'T1_orig' )
  self.linkParameters( 'ribbon_image', 'T1_orig' )
  self.linkParameters( 'Talairach_Auto', 'T1_orig' )
  self.linkParameters( 'Biais_corrected_output', 'T1_output' )
  #self.linkParameters( 'white_ridges', 'T1_output' )
  #self.linkParameters( 'hfiltered', 'T1_output' )
  self.linkParameters( 'Voronoi_output', 'T1_output' )
  self.linkParameters( 'normalization_transformation', 'T1_output' )
  self.linkParameters( 'Talairach_transform', 'T1_output' )
  self.linkParameters( 'histo_analysis', 'Biais_corrected_output' )
  self.linkParameters( 'Rgrey_white_output', 'T1_output' )
  self.linkParameters( 'Lgrey_white_output', 'T1_output' )



def execution( self, context ):
  #Temporary files
  tmp_ori = context.temporary( 'NIFTI-1 image', 'Raw T1 MRI'  )
  tmp_nu = context.temporary( 'NIFTI-1 image', 'T1 MRI Bias Corrected'  )
  tmp_ribbon = context.temporary( 'NIFTI-1 image', 'Voronoi Diagram'  )
  database = self.T1_orig.get('_database')
  
  #Convert the three volumes from .mgz to .nii with Freesurfer
  context.write("Convert .mgz to .nii with FreeSurfer")
  launchFreesurferCommand(context, database, 'mri_convert', '-i', self.T1_orig, '-o', tmp_ori)
  launchFreesurferCommand(context, database, 'mri_convert', '-i', self.nu_image, '-o', tmp_nu)
  launchFreesurferCommand(context, database, 'mri_convert', '-i', self.ribbon_image, '-o', tmp_ribbon)

  #Import Data 
  context.write("Import Data into database with brainvisa ontology")
  context.write(database)
  #context.runProcess( 'ImportT1MRI', input=self.T1_orig, output=self.T1_output)
  context.runProcess( 'ImportT1MRI', input=tmp_ori, output=self.T1_output)
  #context.runProcess( 'ImportGenericVolume', self.nu_image , self.Biais_corrected_output)
  context.runProcess( 'ImportData', tmp_nu , self.Biais_corrected_output)
  #context.runProcess( 'ImportGenericVolume', tmp_ribbon , self.Voronoi_output)
  context.runProcess( 'ImportData', tmp_ribbon , self.Voronoi_output)
  
  
  #Convert .xfm and create ACPC file
  #mniReferential = trManager.referential(registration.talairachMNIReferentialId )
  if self.Talairach_Auto is not None:
    # import / convert transformation to MNI space
    #context.write( _t_( 'import transformation' ) )
    context.write("Convert Talairach_Auto into AC-PC File")
    m = []
    i = 0
    rl = False 
    for l in open( self.Talairach_Auto.fullPath() ).xreadlines():
      print l
      if l.startswith( 'Linear_Transform =' ):
	rl = True
      elif rl:
	if l.endswith( ';\n' ):
	  l = l[:-2]
	  print l
	m.append( [ float(x) for x in l.split() ] )
	i += 1
	if i == 3:
	  break

    talairach_freesrufer = aims.AffineTransformation3d( numpy.array( m  + [[ 0., 0., 0., 1. ]] ) )
    print shfjGlobals.aimsVolumeAttributes( tmp_ori)[ 'transformations' ]
    header_nifti =  aims.AffineTransformation3d(shfjGlobals.aimsVolumeAttributes(tmp_ori)[ 'transformations' ][-1] )
    t1aims2mni = talairach_freesrufer * header_nifti
    aims.write( t1aims2mni, self.normalization_transformation.fullPath() )

    if self.Talairach_transform is not None:
      trm = context.temporary( 'Transformation matrix' )
      aims.write( t1aims2mni, trm.fullPath() )
      
      context.runProcess( 'TalairachTransformationFromNormalization', self.normalization_transformation,  self.T1_output, self.Talairach_transform, self.T1_output, self.T1_output)


  #VipGreyStatClassif  = self.Voronoi_output
  #change labels for Voronoi
  context.write("Create R/L-Grey white files from ribbon freesurfer data")
  VipGreyStatClassif = context.temporary( 'NIFTI-1 image' )
  context.system( 'AimsReplaceLevel',    '-i',  self.Voronoi_output,    '-o', VipGreyStatClassif ,    '-g', '42', '41', '2', '3', '-n', '100' ,'200', '200', '100' )
  context.system( 'AimsReplaceLevel',    '-i',  self.Voronoi_output,    '-o', self.Rgrey_white_output,    '-g', '42', '41', '2', '3', '-n', '100' ,'200', '0', '0' )
  context.system( 'AimsReplaceLevel',    '-i',  self.Voronoi_output,    '-o', self.Lgrey_white_output,    '-g', '42', '41', '2', '3', '-n', '0' ,'0', '200', '100' )
  
  context.write("Create Voronoi file from ribbon freesurfer data")
  context.system( 'AimsReplaceLevel',    '-i',  self.Voronoi_output,    '-o', self.Voronoi_output,    '-g', '42', '41', '2', '3', '-n', '1' ,'1', '2', '2' )

  #Copy referential
  trManager = registration.getTransformationManager()
  trManager.copyReferential( self.T1_output, self.Voronoi_output )
  trManager.copyReferential( self.T1_output, self.Lgrey_white_output )
  trManager.copyReferential( self.T1_output, self.Rgrey_white_output )

  #Launch VipT1BiaisCorrection
  context.write("Launch T1BiasCorrection")
  context.runProcess( 'T1BiasCorrection', mri=self.T1_output, mri_corrected=self.Biais_corrected_output, Commissure_coordinates=self.Talairach_transform)

  #Launch VipGreyStatFromClassif to generate a histo analysis file
  context.write("Launch VipGreyStatFromClassif to generate a histo analysis file")
  context.system( 'VipGreyStatFromClassif', '-i',  self.Biais_corrected_output, '-c', VipGreyStatClassif, '-a', self.histo_analysis, '-g', '100', '-w','200')


