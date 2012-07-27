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
from brainvisa.processes import *
from brainvisa import shelltools
from brainvisa.validation import ValidationError
import shfjGlobals, stat
from soma import aims
import numpy
import registration
#from freesurfer.brainvisaFreesurfer import launchFreesurferCommand
from freesurfer.brainvisaFreesurfer import *
import threading 
from soma.wip.application.api import Application



configuration = Application().configuration


 
#def validation():
#  pass
   #if ( not configuration.SPM.spm8_standalone_command \
       #or not configuration.SPM.spm8_standalone_mcr_path ) \
       #or not distutils.spawn.find_executable( \
          #configuration.matlab.executable ):
          #raise ValidationError( 'SPM or matlab is not found' )


def delInMainThread( lock, thing ): #Pour pb de communiation avec Anatomist
  lock.acquire()
  del thing
  #print 'deleted'
  lock.release()



name = 'Import From FreeSurfer to T1 pipeline'
roles = ('importer',)
userLevel = 1


def validation():
  pass
  #try:
    #from soma import aims
  #except:
    #raise ValidationError( 'aims module not available' )
  #try:
    #import numpy
  #except:
    #raise ValidationError( 'numpy module not available' )

  #testFreesurferCommand()
  #try: 
    #testFreesurferCommand(self.context)
    #print "retour testFreesurferCommand : "
    #print retour
  #except:
    #raise ValidationError( 'FreeSurfer not available' )
  

signature=Signature(
  'T1_orig', ReadDiskItem( 'T1 FreesurferAnat',  'FreesurferMGZ', exactType=True ),
  #seems no mandatory ?
  #'nu_image', ReadDiskItem( 'Nu FreesurferAnat', 'FreesurferMGZ' ),
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
  'Split_brain_output', WriteDiskItem( 'Split Brain Mask', [ 'GIS image', 'NIFTI-1 image', 'gz compressed NIFTI-1 image' ] ),
  'Rgrey_white_output', WriteDiskItem( 'Right Grey White Mask', [ 'GIS image', 'NIFTI-1 image', 'gz compressed NIFTI-1 image' ] ),
  'Lgrey_white_output', WriteDiskItem( 'Left Grey White Mask', [ 'GIS image', 'NIFTI-1 image', 'gz compressed NIFTI-1 image' ] ),
  # 'input_spm_orientation', Choice( '0', '1', ), 
  #Obsolete with Morphologist 2012
  #'left_hemi_cortex', WriteDiskItem( 'Left CSF+GREY Mask',
  #    'Aims writable volume formats' ),
  #'right_hemi_cortex', WriteDiskItem( 'Right CSF+GREY Mask',
  #    'Aims writable volume formats' ), 
  'use_t1pipeline', Choice( ( 'graphically', 0 ), ( 'in batch', 1 ), ( 'don\'t use it', 2 ) )   
)


def initialization( self ):
  #self.signature[ 'output' ].browseUserLevel = 3
  #self.signature[ 'nu input' ].databaseUserLevel = 2
  #self.linkParameters( 'nu_image', 'T1_orig' )
  self.linkParameters( 'ribbon_image', 'T1_orig' )
  self.linkParameters( 'Talairach_Auto', 'T1_orig' )
  self.linkParameters( 'Biais_corrected_output', 'T1_output' )
  #self.linkParameters( 'white_ridges', 'T1_output' )
  #self.linkParameters( 'hfiltered', 'T1_output' )
  self.linkParameters( 'Split_brain_output', 'T1_output' )
  self.linkParameters( 'normalization_transformation', 'T1_output' )
  self.linkParameters( 'Talairach_transform', 'T1_output' )
  self.linkParameters( 'histo_analysis', 'Biais_corrected_output' )
  #self.linkParameters( 'histo_analysis', 'T1_output' )
  self.linkParameters( 'Rgrey_white_output', 'T1_output' )
  self.linkParameters( 'Lgrey_white_output', 'T1_output' )
  #Obsolete with Morphologist 2012
  #self.linkParameters( 'left_hemi_cortex', 'Biais_corrected_output' )
  #self.linkParameters( 'right_hemi_cortex', 'Biais_corrected_output' )
  



def execution( self, context ):
 #a rajouter ?
  #pi, p = context.getProgressInfo( self )
  #pi.children = [ None ] * 3
  #nsteps = 2

  #Temporary files
  tmp_ori = context.temporary( 'NIFTI-1 image', 'Raw T1 MRI'  )
  #tmp_nu = context.temporary( 'NIFTI-1 image', 'T1 MRI Bias Corrected'  )
  tmp_ribbon = context.temporary( 'NIFTI-1 image', 'Split Brain Mask'  )
  database = self.T1_orig.get('_database')
  
  #Convert the three volumes from .mgz to .nii with Freesurfer
  context.write("Convert .mgz to .nii with FreeSurfer")

  #correct line
  launchFreesurferCommand(context, database, 'mri_convert', '-i', self.T1_orig, '-o', tmp_ori)
  
  #launchFreesurfer(context, database, 'mri_convert', '-i', self.T1_orig, '-o', tmp_ori)
  #cmd = 'freesurfer | mri_convert -i /volatile/TMP/test_config_freesurfer/T1.mgz -o /volatile/TMP/test_config_freesurfer/result_test.nii'
  #context.system(cmd)
  
  
  #launchFreesurferCommand(context, database, 'mri_convert', '-i', self.nu_image, '-o', tmp_nu)
  launchFreesurferCommand(context, database, 'mri_convert', '-i', self.ribbon_image, '-o', tmp_ribbon)

  #Import Data 
  context.write("Import Data into database with brainvisa ontology")
  context.write(database)
  #context.runProcess( 'ImportT1MRI', input=self.T1_orig, output=self.T1_output)
  context.runProcess( 'ImportT1MRI', input=tmp_ori, output=self.T1_output)
  #context.runProcess( 'ImportGenericVolume', self.nu_image , self.Biais_corrected_output)
  
  #context.runProcess( 'ImportData', tmp_nu , self.Biais_corrected_output)
  #context.system( 'AimsFileConvert', '-i',  self.Biais_corrected_output, '-o', self.Biais_corrected_output, '-t', 'S16')
  
  #context.runProcess( 'ImportGenericVolume', tmp_ribbon , self.Split_brain_output)
  context.runProcess( 'ImportData', tmp_ribbon , self.Split_brain_output)
  context.system( 'AimsFileConvert', '-i',  self.Split_brain_output, '-o', self.Split_brain_output, '-t', 'S16')
  
  
  ##Convert .xfm and create ACPC file
  ##mniReferential = trManager.referential(registration.talairachMNIReferentialId )
  #if self.Talairach_Auto is not None:
    ## import / convert transformation to MNI space
    ##context.write( _t_( 'import transformation' ) )
    #context.write("Convert Talairach_Auto into AC-PC File")
    #m = []
    #i = 0
    #rl = False 
    #for l in open( self.Talairach_Auto.fullPath() ).xreadlines():
      #print l
      #if l.startswith( 'Linear_Transform =' ):
	#rl = True
      #elif rl:
	#if l.endswith( ';\n' ):
	  #l = l[:-2]
	  #print l
	#m.append( [ float(x) for x in l.split() ] )
	#i += 1
	#if i == 3:
	  #break

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
    #print shfjGlobals.aimsVolumeAttributes( tmp_ori)[ 'transformations' ]
    header_nifti =  aims.AffineTransformation3d(shfjGlobals.aimsVolumeAttributes(tmp_ori)[ 'transformations' ][-1] )
    t1aims2mni = talairach_freesrufer * header_nifti
    aims.write( t1aims2mni, self.normalization_transformation.fullPath() )

    if self.Talairach_transform is not None:
      trm = context.temporary( 'Transformation matrix' )
      aims.write( t1aims2mni, trm.fullPath() )
      
      context.runProcess( 'TalairachTransformationFromNormalization', self.normalization_transformation,  self.T1_output, self.Talairach_transform, self.T1_output, self.T1_output)


  #VipGreyStatClassif  = self.Split_brain_output
  #change labels for Split Brain
  context.write("Create R/L-Grey white files from ribbon freesurfer data")
  VipGreyStatClassif = context.temporary( 'NIFTI-1 image' )
  context.system( 'AimsReplaceLevel',    '-i',  self.Split_brain_output,    '-o', VipGreyStatClassif ,    '-g', '42', '41', '2', '3', '-n', '100' ,'200', '200', '100' )
  context.system( 'AimsReplaceLevel',    '-i',  self.Split_brain_output,    '-o', self.Rgrey_white_output,    '-g', '42', '41', '2', '3', '-n', '100' ,'200', '0', '0' )
  context.system( 'AimsReplaceLevel',    '-i',  self.Split_brain_output,    '-o', self.Lgrey_white_output,    '-g', '42', '41', '2', '3', '-n', '0' ,'0', '200', '100' )
  
  context.write("Create Split Brain file from ribbon freesurfer data")
  context.system( 'AimsReplaceLevel',    '-i',  self.Split_brain_output,    '-o', self.Split_brain_output,    '-g', '42', '41', '2', '3', '-n', '1' ,'1', '2', '2' )

  #Copy referential
  trManager = registration.getTransformationManager()
  trManager.copyReferential( self.T1_output, self.Split_brain_output )
  trManager.copyReferential( self.T1_output, self.Lgrey_white_output )
  trManager.copyReferential( self.T1_output, self.Rgrey_white_output )

  #Launch VipT1BiaisCorrection
  context.write("Launch T1BiasCorrection")
  

  #On doit indiquer les valeurs de write_hfiltered et write_wridges à no maintenant ?
  context.runProcess( 'T1BiasCorrection', mri=self.T1_output, mri_corrected=self.Biais_corrected_output, Commissure_coordinates=self.Talairach_transform)

  #Launch VipGreyStatFromClassif to generate a histo analysis file
  context.write("Launch VipGreyStatFromClassif to generate a histo analysis file")
  context.system( 'VipGreyStatFromClassif', '-i',  self.Biais_corrected_output, '-c', VipGreyStatClassif, '-a', self.histo_analysis, '-g', '100', '-w','200')

  

  #Obsolete with Morphologist 2012
  ##Histo temporaire pour segmentaiton du cortex
  #han = context.temporary( 'Histo Analysis' )
  #open( han.fullPath(), 'w' ).write( \
  #'''sequence: unknown
  #csf: mean: -1 sigma: -1
  #gray: mean: 100 sigma: 1
  #white: mean: 200 sigma: 1
  #''' )
  
  
  #Obsolete with Morphologist 2012
  ##Segmentation du cortex : Lcortex_subject
  #Lbraing = context.temporary( 'GIS Image' )
  #context.system( 'VipMask', '-i', self.Lgrey_white_output, "-m",
                  #self.Split_brain_output, "-o", Lbraing, "-w",
                  #"t", "-l", "2" )
  #context.system( "VipHomotopicSnake", "-i", Lbraing, "-h",
                  #han, "-o", self.left_hemi_cortex, "-w", "t" )
  #trManager.copyReferential(self.Biais_corrected_output, self.left_hemi_cortex)
  
  
  ##Segmentation du cortex : Rcortex_subject
  #Rbraing = context.temporary( 'GIS Image' )
  #context.system( "VipMask", "-i", self.Rgrey_white_output, "-m",
                  #self.Split_brain_output, "-o", Rbraing,
                  #"-w", "t", "-l", "1" )
  #context.system( "VipHomotopicSnake", "-i", Rbraing, "-h",
                  #han, "-o", self.right_hemi_cortex, "-w", "t" )
  #trManager.copyReferential(self.Biais_corrected_output, self.right_hemi_cortex)
  #end of obsolete with Morphologist 2012


  #Lock Data
  self.T1_output.lockData()
  self.Biais_corrected_output.lockData()
  self.normalization_transformation.lockData()
  self.Talairach_transform.lockData() 
  self.histo_analysis.lockData()
  self.Split_brain_output.lockData()
  self.Rgrey_white_output.lockData()
  self.Lgrey_white_output.lockData()
  #Obsolete with Morphologist 2012
  #self.left_hemi_cortex.lockData()
  #self.right_hemi_cortex.lockData()
 


  #Launch Morphologist
  t1pipeline = getProcessInstance( 'morphologist' )
  t1pipeline.mri = self.T1_output
  
  t1pipeline.mri_corrected = self.Biais_corrected_output
  
  enode = t1pipeline.executionNode()
  
  #npi, proc = context.getProgressInfo( enode, parent=pi )
  
  #context.progress()


  context.write( _t_( 'Now run the last part of the regular T1 pipeline.' ) )
  
  
  enode.PrepareSubject.setSelected( False )
  enode.BiasCorrection.setSelected( False )
  enode.HistoAnalysis.setSelected( False )
  enode.BrainSegmentation.setSelected( False )
  enode.SplitBrain.setSelected( False )
  enode.TalairachTransformation.setSelected( False )
  
  #enode.GreyWhiteInterface.setSelected( True )
  #enode.GreyWhiteInterface.GreyWhiteInterface.setSelected( False )
  #For Morphologist 2012
  enode.GreyWhiteClassification.setSelected( False )
  #enode.GreyWhiteInterface.cortex_image.setSelected( False )
  #enode.GreyWhiteInterface.GreyWhiteMesh.GreyWhiteInterface05.setSelected( True )
  #For Morphologist 2012
  enode.GreyWhiteSurface.setSelected( True )
  
  enode.HemispheresMesh.setSelected( True )
  enode.HeadMesh.setSelected( True )
  enode.CorticalFoldsGraph.setSelected( True )
  # we _must_ build 3.1 graphs because 3.0 overwrite cortex images
  # now we could use 3.0 graph thanks to Morpho 2012 but it seems a good choice to keep 
  #3.1 even if it is not the default value in Mropho 2012
  enode.CorticalFoldsGraph.CorticalFoldsGraph_3_1.setSelected( True )



  if self.use_t1pipeline == 0:
    pv = mainThreadActions().call( ProcessView, t1pipeline )
    r = context.ask( 'run the pipeline, then click here', 'OK' )
    #print '***************** OK clicked'
    mainThreadActions().call( pv.close )
    lock = threading.Lock()
    lock.acquire()
    mainThreadActions().push( delInMainThread, lock, pv )
    del pv
    #print '*** DELETED'
    lock.release()
    #print 'lock released'
  elif self.use_t1pipeline == 1:
    context.runProcess( t1pipeline )
  else:
    context.write( '<font color="#a0a060">' \
      + _t_( 'Pipeline not run since the "use_t1pipeline" parameter ' \
        'prevents it' ) + '</font>')
  
  context.write( 'OK')
  #context.progress( 10, nsteps, self )
  








