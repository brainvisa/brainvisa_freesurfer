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
from brainvisa.tools import aimsGlobals
import stat
from soma import aims
import numpy
from brainvisa import registration
from freesurfer.brainvisaFreesurfer import *
import threading 
from soma.wip.application.api import Application



configuration = Application().configuration


def delInMainThread( lock, thing ): #Pour pb de communiation avec Anatomist
  lock.acquire()
  del thing
  lock.release()

  
name = 'Import From FreeSurfer to T1 pipeline'
roles = ('importer',)
userLevel = 1


def validation():
  pass

signature=Signature(
  'T1_orig', ReadDiskItem( 'T1 FreesurferAnat',  'FreesurferMGZ', exactType=True ),
  #seems no mandatory ?
  'ribbon_image', ReadDiskItem( 'Ribbon Freesurfer', 'FreesurferMGZ' ),
  'scanner_based_referential', ReadDiskItem( 'Scanner Based Referential', 'Referential' ),
  'Talairach_Auto', ReadDiskItem( 'Talairach Auto Freesurfer', 'MINC transformation matrix' ), 
  'T1_output', WriteDiskItem( 'Raw T1 MRI', [ 'GIS image', 'NIFTI-1 image', 'gz compressed NIFTI-1 image' ] ),
  'T1_referential', WriteDiskItem( 'Referential of Raw T1 MRI', 'Referential' ),
  'transform_to_scanner_based', WriteDiskItem( 'Transformation to Scanner Based Referential', 'Transformation matrix' ),
  'Bias_corrected_output', WriteDiskItem( 'T1 MRI Bias Corrected', [ 'GIS image', 'NIFTI-1 image', 'gz compressed NIFTI-1 image' ] ),
  'normalization_transformation',  WriteDiskItem( 'Transform Raw T1 MRI to Talairach-MNI template-SPM', 'Transformation matrix' ), 
  'Talairach_transform',  WriteDiskItem( 'Transform Raw T1 MRI to Talairach-AC/PC-Anatomist', 'Transformation matrix' ),
  'commissure_coordinates', WriteDiskItem( 'Commissure Coordinates', 'Commissure coordinates' ),
  'histo_analysis', WriteDiskItem( 'Histo Analysis', 'Histo Analysis' ),
  'Split_brain_output', WriteDiskItem( 'Split Brain Mask', [ 'GIS image', 'NIFTI-1 image', 'gz compressed NIFTI-1 image' ] ),
  'Rgrey_white_output', WriteDiskItem( 'Right Grey White Mask', [ 'GIS image', 'NIFTI-1 image', 'gz compressed NIFTI-1 image' ] ),
  'Lgrey_white_output', WriteDiskItem( 'Left Grey White Mask', [ 'GIS image', 'NIFTI-1 image', 'gz compressed NIFTI-1 image' ] ),
  'use_t1pipeline', Choice( ( 'graphically', 0 ), ( 'in batch', 1 ), ( 'don\'t use it', 2 ) ),
  'mni_referential', ReadDiskItem( 'Referential', 'Referential' ),
  'transform_chain_ACPC_to_Normalized',  ListOf( ReadDiskItem( 'Transformation', 'Transformation matrix' ) ),
  'acpc_referential', ReadDiskItem('Referential', 'Referential'),
  'bias_field', WriteDiskItem( 'T1 MRI bias field', 'aims writable volume formats' ),
  'hfiltered', WriteDiskItem( 'T1 MRI filtered for histo', 'aims writable volume formats' ),
  'white_ridges', WriteDiskItem( 'T1 MRI white matter ridges', 'aims writable volume formats', exactType=True ),
  'mean_curvature', WriteDiskItem( 'T1 MRI mean curvature', 'aims writable volume formats' ),
  'variance', WriteDiskItem( 'T1 MRI variance', 'aims writable volume formats' ),
  'edges', WriteDiskItem( 'T1 MRI edges', 'aims writable volume formats' ),
)


def initialization( self ):

  def linkACPC_to_norm( proc, param ):
    trManager = registration.getTransformationManager()
    if proc.mni_referential:
      try:
        id = proc.mni_referential.uuid()
      except:
        return []
      _mniToACPCpaths = trManager.findPaths( \
        registration.talairachACPCReferentialId, id )
      for x in _mniToACPCpaths:
        return x
      else:
        return []

  #self.signature[ 'output' ].browseUserLevel = 3
  #self.signature[ 'nu input' ].databaseUserLevel = 2
  self.linkParameters( 'ribbon_image', 'T1_orig' )
  self.linkParameters( 'scanner_based_referential', 'T1_orig' )
  self.linkParameters( 'Talairach_Auto', 'T1_orig' )
  self.linkParameters( 'transform_to_scanner_based', 'T1_output' )
  self.linkParameters( 'Bias_corrected_output', 'T1_output' )
  self.linkParameters( 'Split_brain_output', 'T1_output' )
  self.linkParameters( 'normalization_transformation', 'T1_output' )
  self.linkParameters( 'Talairach_transform', 'T1_output' )
  self.linkParameters( 'histo_analysis', 'Bias_corrected_output' )
  self.linkParameters( 'Rgrey_white_output', 'T1_output' )
  self.linkParameters( 'Lgrey_white_output', 'T1_output' )
  self.linkParameters( 'T1_referential', 'T1_output' )
  self.linkParameters( 'commissure_coordinates', 'T1_output' )
  self.linkParameters( 'transform_chain_ACPC_to_Normalized',
    'mni_referential', linkACPC_to_norm )
  trManager = registration.getTransformationManager()
  self.mni_referential = trManager.referential(
    registration.talairachMNIReferentialId )
  self.acpc_referential = trManager.referential(
    registration.talairachACPCReferentialId )
  self.use_t1pipeline = 1
  self.linkParameters( 'bias_field', 'T1_output' )
  self.linkParameters( 'hfiltered', 'T1_output' )
  self.linkParameters( 'white_ridges', 'T1_output' )
  self.linkParameters( 'mean_curvature', 'T1_output' )
  self.linkParameters( 'variance', 'T1_output' )
  self.linkParameters( 'edges', 'T1_output' )
  self.setOptional( 'scanner_based_referential', 'transform_to_scanner_based' )
  self.signature['mni_referential'].userLevel = 2
  self.signature['transform_chain_ACPC_to_Normalized'].userLevel = 2
  self.signature['acpc_referential'].userLevel = 2
  self.signature['bias_field'].userLevel = 2
  self.signature['hfiltered'].userLevel = 2
  self.signature['white_ridges'].userLevel = 2
  self.signature['mean_curvature'].userLevel = 2
  self.signature['variance'].userLevel = 2
  self.signature['edges'].userLevel = 2


def execution( self, context ):
 #a rajouter ?
  #pi, p = context.getProgressInfo( self )
  #pi.children = [ None ] * 3
  #nsteps = 2

  #Temporary files
  tmp_ori = context.temporary( 'NIFTI-1 image', 'Raw T1 MRI'  )
  tmp_ribbon = context.temporary( 'NIFTI-1 image', 'Split Brain Mask'  )
  database = ''

  #Convert the three volumes from .mgz to .nii with Freesurfer
  context.write("Convert .mgz to .nii with FreeSurfer")

  #correct line
  launchFreesurferCommand(context, database, 'mri_convert', '-i', self.T1_orig,
    '-o', tmp_ori)

  launchFreesurferCommand(context, database, 'mri_convert',
    '-i', self.ribbon_image, '-o', tmp_ribbon)

  #Import Data 
  context.write("Import Data into database with brainvisa ontology")
  context.write(database)
  context.runProcess( 'ImportT1MRI', input=tmp_ori, output=self.T1_output)

  if self.transform_to_scanner_based is not None:
    t1h = aimsGlobals.aimsVolumeAttributes( self.T1_output )
    tr = aims.AffineTransformation3d( t1h[ 'transformations' ][-1] )
    tr.header()[ 'source_referential' ] = str( self.T1_referential.uuid() )
    if self.scanner_based_referential is not None:
      tr.header()[ 'destination_referential' ] \
        = str( self.scanner_based_referential.uuid() )
    aims.write( tr, self.transform_to_scanner_based.fullPath() )
    self.transform_to_scanner_based.readAndUpdateMinf()

  context.runProcess( 'ImportData', tmp_ribbon , self.Split_brain_output)
  context.system( 'AimsFileConvert', '-i',  self.Split_brain_output,
    '-o', self.Split_brain_output, '-t', 'S16')

  if self.Talairach_Auto is not None:
    # import / convert transformation to MNI space
    #context.write( _t_( 'import transformation' ) )
    context.write("Convert Talairach_Auto into AC-PC File")
    m = []
    i = 0
    rl = False
    for l in open( self.Talairach_Auto.fullPath() ).xreadlines():
      if l.startswith( 'Linear_Transform =' ):
        rl = True
      elif rl:
        if l.endswith( ';\n' ):
          l = l[:-2]
        m.append( [ float(x) for x in l.split() ] )
        i += 1
        if i == 3:
          break

    talairach_freesurfer = aims.AffineTransformation3d(
      numpy.array( m  + [[ 0., 0., 0., 1. ]] ) )
    header_nifti =  aims.AffineTransformation3d(aimsGlobals.aimsVolumeAttributes(tmp_ori)[ 'transformations' ][-1] )
    t1aims2mni = talairach_freesurfer * header_nifti
    aims.write( t1aims2mni, self.normalization_transformation.fullPath() )
    self.normalization_transformation.setMinf( 'source_referential',
      str( self.T1_referential.uuid() ), saveMinf=True )
    self.normalization_transformation.setMinf( 'destination_referential',
      str( registration.talairachMNIReferentialId ), saveMinf=True )

    if self.Talairach_transform is not None:
      trm = context.temporary( 'Transformation matrix' )
      aims.write( t1aims2mni, trm.fullPath() )

      context.runProcess( 'TalairachTransformationFromNormalization',
        normalization_transformation=self.normalization_transformation,
        Talairach_transform=self.Talairach_transform,
        commissure_coordinates=self.commissure_coordinates,
        t1mri=self.T1_output, source_referential=self.T1_referential,
        normalized_referential=self.mni_referential,
        transform_chain_ACPC_to_Normalized=self.transform_chain_ACPC_to_Normalized,
        acpc_referential=self.acpc_referential )


  #change labels for Split Brain
  context.write("Create R/L-Grey white files from ribbon freesurfer data")
  VipGreyStatClassif = context.temporary( 'NIFTI-1 image' )
  context.system( 'AimsReplaceLevel',
                  '-i', self.Split_brain_output,
                  '-o', VipGreyStatClassif ,
                  '-g', '42', '41', '2', '3',
                  '-n', '100', '200', '200', '100' )
  context.system( 'AimsReplaceLevel',
                  '-i', self.Split_brain_output,
                  '-o', self.Rgrey_white_output,
                  '-g', '42', '41', '2', '3',
                  '-n', '100', '200', '0', '0' )
  context.system( 'AimsReplaceLevel',
                  '-i', self.Split_brain_output,
                  '-o', self.Lgrey_white_output,
                  '-g', '42', '41', '2', '3',
                  '-n', '0', '0', '200', '100' )
  
  context.write("Create Split Brain file from ribbon freesurfer data")
  context.system( 'AimsReplaceLevel',
                  '-i', self.Split_brain_output,
                  '-o', self.Split_brain_output,
                  '-g', '42', '41', '2', '3',
                  '-n', '1', '1', '2', '2' )

  #Copy referential
  trManager = registration.getTransformationManager()
  trManager.copyReferential( self.T1_output, self.Split_brain_output )
  trManager.copyReferential( self.T1_output, self.Lgrey_white_output )
  trManager.copyReferential( self.T1_output, self.Rgrey_white_output )

  #Launch VipT1BiaisCorrection
  context.write("Launch T1BiasCorrection")

  context.runProcess( 'T1BiasCorrection', t1mri=self.T1_output,
    t1mri_nobias=self.Bias_corrected_output,
    field=self.bias_field,
    hfiltered=self.hfiltered,
    white_ridges=self.white_ridges,
    meancurvature=self.mean_curvature,
    variance=self.variance,
    edges=self.edges,
    commissure_coordinates=self.commissure_coordinates)

  #Launch VipGreyStatFromClassif to generate a histo analysis file
  context.write("Launch VipGreyStatFromClassif to generate a histo analysis file")
  context.system( 'VipGreyStatFromClassif',
                  '-i', self.Bias_corrected_output,
                  '-c', VipGreyStatClassif,
                  '-a', self.histo_analysis,
                  '-g', '100', '-w','200')

  #Lock Data
  self.T1_output.lockData()
  self.Bias_corrected_output.lockData()
  self.normalization_transformation.lockData()
  self.Talairach_transform.lockData() 
  self.histo_analysis.lockData()
  self.Split_brain_output.lockData()
  self.Rgrey_white_output.lockData()
  self.Lgrey_white_output.lockData()


  #Launch Morphologist
  if self.use_t1pipeline != 2:
    t1pipeline = getProcessInstance( 'morphologist' )
    
    t1pipeline.t1mri = self.T1_output
    t1pipeline.t1mri_nobias = self.Bias_corrected_output
    t1pipeline.histo_analysis = self.histo_analysis
    t1pipeline.split_brain = self.Split_brain_output

    enode = t1pipeline.executionNode()

    context.write( _t_( 'Now run the last part of the regular T1 pipeline.' ) )


    enode.PrepareSubject.setSelected( False )
    enode.BiasCorrection.setSelected( False )
    enode.HistoAnalysis.setSelected( False )
    enode.BrainSegmentation.setSelected( False )
    enode.SplitBrain.setSelected( False )
    enode.TalairachTransformation.setSelected( False )
    enode.HeadMesh.setSelected( True )
    enode.HemispheresProcessing.setSelected( True )
    enode.HemispheresProcessing.LeftHemisphere.setSelected( True )
    enode.HemispheresProcessing.LeftHemisphere.GreyWhiteClassification.setSelected( False )
    enode.HemispheresProcessing.LeftHemisphere.GreyWhiteTopology.setSelected( True )
    enode.HemispheresProcessing.LeftHemisphere.GreyWhiteMesh.setSelected( True )
    enode.HemispheresProcessing.LeftHemisphere.SulciSkeleton.setSelected( True )
    enode.HemispheresProcessing.LeftHemisphere.PialMesh.setSelected( True )
    enode.HemispheresProcessing.LeftHemisphere.CorticalFoldsGraph.setSelected( True )
    enode.HemispheresProcessing.RightHemisphere.setSelected( True )
    enode.HemispheresProcessing.RightHemisphere.GreyWhiteClassification.setSelected( False )
    enode.HemispheresProcessing.RightHemisphere.GreyWhiteTopology.setSelected( True )
    enode.HemispheresProcessing.RightHemisphere.GreyWhiteMesh.setSelected( True )
    enode.HemispheresProcessing.RightHemisphere.SulciSkeleton.setSelected( True )
    enode.HemispheresProcessing.RightHemisphere.PialMesh.setSelected( True )
    enode.HemispheresProcessing.RightHemisphere.CorticalFoldsGraph.setSelected( True )

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

