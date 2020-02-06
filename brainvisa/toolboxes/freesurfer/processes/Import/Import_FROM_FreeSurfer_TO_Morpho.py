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

from __future__ import print_function

from freesurfer.brainvisaFreesurfer import *
from brainvisa.processes import *
from brainvisa.tools import aimsGlobals
from brainvisa import registration
from soma import aims
import numpy
import threading


def delInMainThread(lock, thing):  # Pour pb de communiation avec Anatomist
    lock.acquire()
    del thing
    lock.release()


name = 'Import FreeSurfer grey/white segmentation to Morphologist'
roles = ('importer',)
userLevel = 0


signature = Signature(
    'T1_orig', ReadDiskItem('T1 FreesurferAnat',
                            'FreesurferMGZ',
                            exactType=True),
  'ribbon_image', ReadDiskItem('Ribbon Freesurfer',
                               'FreesurferMGZ',
                               requiredAttributes={'side': 'both',
                                                   'space': 'freesurfer analysis'}),
  'scanner_based_referential', ReadDiskItem('Scanner Based Referential',
                                            'Referential'),
  'Talairach_Auto', ReadDiskItem('Talairach Auto Freesurfer',
                                 'MINC transformation matrix'),
  'T1_output', WriteDiskItem('Raw T1 MRI',
                             ['gz compressed NIFTI-1 image',
                              'NIFTI-1 image',
                              'GIS image']),
  'T1_referential', WriteDiskItem('Referential of Raw T1 MRI',
                                  'Referential'),
  'transform_to_scanner_based', WriteDiskItem('Transformation to Scanner Based Referential',
                                              'Transformation matrix'),
  'bias_corrected_output', WriteDiskItem('T1 MRI Bias Corrected',
                                         'Aims writable volume formats'),
  'normalization_transformation', WriteDiskItem('Transform Raw T1 MRI to Talairach-MNI template-SPM',
                                                'Transformation matrix'),
  'talairach_transform', WriteDiskItem('Transform Raw T1 MRI to Talairach-AC/PC-Anatomist',
                                       'Transformation matrix'),
  'commissure_coordinates', WriteDiskItem('Commissure Coordinates',
                                          'Commissure coordinates'),
  'histo_analysis', WriteDiskItem('Histo Analysis',
                                  'Histo Analysis'),
  'brain_mask_output', WriteDiskItem('T1 Brain Mask',
                                     'Aims writable volume formats'),
  'split_brain_output', WriteDiskItem('Split Brain Mask',
                                      'Aims writable volume formats'),
  'right_grey_white_output', WriteDiskItem('Right Grey White Mask',
                                           'Aims writable volume formats'),
  'left_grey_white_output', WriteDiskItem('Left Grey White Mask',
                                          'Aims writable volume formats'),
  'use_morphologist', Choice(('graphically', 0),
                             ('in batch', 1),
                             ('don\'t use it', 2)),
  'mni_referential', ReadDiskItem('Referential',
                                  'Referential'),
  'transform_chain_ACPC_to_Normalized', ListOf(ReadDiskItem('Transformation',
                                                            'Transformation matrix')),
  'acpc_referential', ReadDiskItem('Referential',
                                   'Referential'),
)


def initialization(self):

    def linkACPC_to_norm(proc, param):
        trManager = registration.getTransformationManager()
        if proc.mni_referential:
            try:
                id = proc.mni_referential.uuid()
            except:
                return []
            _mniToACPCpaths = trManager.findPaths(
                registration.talairachACPCReferentialId, id)
            for x in _mniToACPCpaths:
                return x
            else:
                return []

    self.linkParameters('ribbon_image', 'T1_orig')
    self.linkParameters('scanner_based_referential', 'T1_orig')
    self.linkParameters('Talairach_Auto', 'T1_orig')
    self.linkParameters('transform_to_scanner_based', 'T1_output')
    self.linkParameters('bias_corrected_output', 'T1_output')
    self.linkParameters('brain_mask_output', 'T1_output')
    self.linkParameters('split_brain_output', 'T1_output')
    self.linkParameters('normalization_transformation', 'T1_output')
    self.linkParameters('talairach_transform', 'T1_output')
    self.linkParameters('histo_analysis', 'bias_corrected_output')
    self.linkParameters('right_grey_white_output', 'T1_output')
    self.linkParameters('left_grey_white_output', 'T1_output')
    self.linkParameters('T1_referential', 'T1_output')
    self.linkParameters('commissure_coordinates', 'T1_output')
    self.linkParameters('transform_chain_ACPC_to_Normalized',
                        'mni_referential',
                        linkACPC_to_norm)
    trManager = registration.getTransformationManager()
    self.mni_referential = trManager.referential(
        registration.talairachMNIReferentialId)
    self.acpc_referential = trManager.referential(
        registration.talairachACPCReferentialId)

    self.use_morphologist = 1
    self.setOptional('scanner_based_referential', 'transform_to_scanner_based')
    self.signature['mni_referential'].userLevel = 2
    self.signature['transform_chain_ACPC_to_Normalized'].userLevel = 2
    self.signature['acpc_referential'].userLevel = 2


def execution(self, context):

    # Temporary files
    tmp_ori = context.temporary('NIFTI-1 image', 'Raw T1 MRI')
    tmp_ribbon = context.temporary('NIFTI-1 image', 'Split Brain Mask')
    database = ''

    # Convert the three volumes from .mgz to .nii with Freesurfer
    context.write("Convert .mgz to .nii with FreeSurfer")

    conv = context.getConverter(self.T1_orig, self.tmp_ori)
    if conv is None:
        raise ValidationError(
            'No converter could be found to convert FreeSurfer MGZ format')
    context.write('MGZ converter found:', conv.name)
    context.runProcess(conv, self.T1_orig, self.tmp_ori)
    context.runProcess(conv, self.ribbon_image, self.tmp_ribbon)

    # launchFreesurferCommand(context, database, 'mri_convert', '-i', self.T1_orig,
        #'-o', tmp_ori)

    # launchFreesurferCommand(context, database, 'mri_convert',
        #'-i', self.ribbon_image, '-o', tmp_ribbon)

    # Import Data
    context.write("Import data into database with brainvisa ontology")
    context.write(database)
    context.runProcess('ImportT1MRI', input=tmp_ori, output=self.T1_output)

    if self.transform_to_scanner_based is not None:
        t1h = aimsGlobals.aimsVolumeAttributes(self.T1_output)
        tr = aims.AffineTransformation3d(t1h['transformations'][-1])
        tr.header()['source_referential'] = str(self.T1_referential.uuid())
        if self.scanner_based_referential is not None:
            tr.header()[ 'destination_referential' ] \
                = str(self.scanner_based_referential.uuid())
        aims.write(tr, self.transform_to_scanner_based.fullPath())
        self.transform_to_scanner_based.readAndUpdateMinf()

    context.runProcess('ImportData', tmp_ribbon, self.split_brain_output)
    context.system('AimsFileConvert', '-i',  self.split_brain_output,
                   '-o', self.split_brain_output, '-t', 'S16')

    if self.Talairach_Auto is not None:
        # import / convert transformation to MNI space
        # context.write( _t_( 'import transformation' ) )
        context.write("Convert Talairach_Auto into AC-PC File")
        m = []
        i = 0
        rl = False
        for l in open(self.Talairach_Auto.fullPath()).xreadlines():
            if l.startswith('Linear_Transform ='):
                rl = True
            elif rl:
                if l.endswith(';\n'):
                    l = l[:-2]
                m.append([float(x) for x in l.split()])
                i += 1
                if i == 3:
                    break

        talairach_freesurfer = aims.AffineTransformation3d(
            numpy.array(m + [[0., 0., 0., 1.]]))
        header_nifti = aims.AffineTransformation3d(
            aimsGlobals.aimsVolumeAttributes(tmp_ori)['transformations'][-1])
        t1aims2mni = talairach_freesurfer * header_nifti
        aims.write(t1aims2mni, self.normalization_transformation.fullPath())
        self.normalization_transformation.setMinf('source_referential',
                                                  str(self.T1_referential.uuid()), saveMinf=True)
        self.normalization_transformation.setMinf('destination_referential',
                                                  str(registration.talairachMNIReferentialId), saveMinf=True)

        if self.talairach_transform is not None:
            trm = context.temporary('Transformation matrix')
            aims.write(t1aims2mni, trm.fullPath())

            context.runProcess('TalairachTransformationFromNormalization',
                               normalization_transformation=self.normalization_transformation,
                               Talairach_transform=self.talairach_transform,
                               commissure_coordinates=self.commissure_coordinates,
                               t1mri=self.T1_output, source_referential=self.T1_referential,
                               normalized_referential=self.mni_referential,
                               transform_chain_ACPC_to_Normalized=self.transform_chain_ACPC_to_Normalized,
                               acpc_referential=self.acpc_referential)

    # change labels for Split Brain
    context.write(
        "Create right/left grey white files from ribbon freesurfer data")
    VipGreyStatClassif = context.temporary('NIFTI-1 image')
    context.system('AimsReplaceLevel',
                   '-i', self.split_brain_output,
                   '-o', VipGreyStatClassif,
                   '-g', '42', '41', '2', '3', '110', '120', '10', '20',
                   '-n', '100', '200', '200', '100',
                   '100', '200', '100', '200')
    context.system('AimsReplaceLevel',
                   '-i', self.split_brain_output,
                   '-o', self.right_grey_white_output,
                   '-g', '42', '41', '2', '3', '110', '120', '10', '20',
                   '-n', '100', '200', '0', '0', '100', '200', '0', '0')
    context.system('AimsReplaceLevel',
                   '-i', self.split_brain_output,
                   '-o', self.left_grey_white_output,
                   '-g', '42', '41', '2', '3', '110', '120', '10', '20',
                   '-n', '0', '0', '200', '100', '0', '0', '100', '200')

    context.write("Create brain mask file from ribbon freesurfer data")
    context.system('AimsReplaceLevel',
                   '-i', self.split_brain_output,
                   '-o', self.brain_mask_output,
                   '-g', '42', '41', '2', '3', '110', '120', '10', '20',
                   '-n', '255', '255', '255', '255', '255', '255', '255', '255')

    context.write("Create split brain file from ribbon freesurfer data")
    context.system('AimsReplaceLevel',
                   '-i', self.split_brain_output,
                   '-o', self.split_brain_output,
                   '-g', '42', '41', '2', '3', '110', '120', '10', '20',
                   '-n', '1', '1', '2', '2', '1', '1', '2', '2')

    # Copy referential
    trManager = registration.getTransformationManager()
    trManager.copyReferential(self.T1_output, self.brain_mask_output)
    trManager.copyReferential(self.T1_output, self.split_brain_output)
    trManager.copyReferential(self.T1_output, self.left_grey_white_output)
    trManager.copyReferential(self.T1_output, self.right_grey_white_output)

    # Launch VipT1BiaisCorrection
    context.write("Launch T1BiasCorrection")
    tmp = context.temporary('NIFTI-1 image')

    context.runProcess('T1BiasCorrection',
                       t1mri=self.T1_output,
                       commissure_coordinates=self.commissure_coordinates,
                       delete_last_n_slices='0',
                       t1mri_nobias=self.bias_corrected_output,
                       field='',
                       write_hfiltered='no',
                       hfiltered=tmp,
                       write_wridges='no',
                       white_ridges=tmp,
                       write_variance='no',
                       variance=tmp,
                       write_edges='no',
                       edges=tmp,
                       meancurvature='')

    # Launch VipGreyStatFromClassif to generate a histo analysis file
    context.write(
        "Launch VipGreyStatFromClassif to generate a histo analysis file")
    context.system('VipGreyStatFromClassif',
                   '-i', self.bias_corrected_output,
                   '-c', VipGreyStatClassif,
                   '-a', self.histo_analysis,
                   '-g', '100', '-w', '200')

    # Lock Data
    self.T1_output.lockData()
    self.bias_corrected_output.lockData()
    self.normalization_transformation.lockData()
    self.talairach_transform.lockData()
    self.histo_analysis.lockData()
    self.brain_mask_output.lockData()
    self.split_brain_output.lockData()
    self.right_grey_white_output.lockData()
    self.left_grey_white_output.lockData()

    # Launch Morphologist
    if self.use_morphologist != 2:
        morphologist = getProcessInstance('morphologist')

        morphologist.t1mri = self.T1_output
        morphologist.t1mri_nobias = self.bias_corrected_output
        morphologist.histo_analysis = self.histo_analysis
        morphologist.split_brain = self.split_brain_output

        enode = morphologist.executionNode()

        context.write(
            _t_('Now run the last part of the regular Morphologist pipeline.'))

        enode.PrepareSubject.setSelected(False)
        enode.BiasCorrection.setSelected(False)
        enode.HistoAnalysis.setSelected(False)
        enode.BrainSegmentation.setSelected(False)
        enode.Renorm.setSelected(False)
        enode.SplitBrain.setSelected(False)
        enode.TalairachTransformation.setSelected(False)
        enode.HeadMesh.setSelected(False)
        enode.HemispheresProcessing.setSelected(True)
        enode.HemispheresProcessing.LeftHemisphere.setSelected(True)
        enode.HemispheresProcessing.LeftHemisphere.GreyWhiteClassification.setSelected(
            False)
        enode.HemispheresProcessing.LeftHemisphere.GreyWhiteTopology.setSelected(
            True)
        enode.HemispheresProcessing.LeftHemisphere.GreyWhiteMesh.setSelected(
            True)
        enode.HemispheresProcessing.LeftHemisphere.SulciSkeleton.setSelected(
            True)
        enode.HemispheresProcessing.LeftHemisphere.PialMesh.setSelected(True)
        enode.HemispheresProcessing.LeftHemisphere.CorticalFoldsGraph.setSelected(
            True)
        enode.HemispheresProcessing.LeftHemisphere.SulciRecognition.setSelected(
            True)
        enode.HemispheresProcessing.RightHemisphere.setSelected(True)
        enode.HemispheresProcessing.RightHemisphere.GreyWhiteClassification.setSelected(
            False)
        enode.HemispheresProcessing.RightHemisphere.GreyWhiteTopology.setSelected(
            True)
        enode.HemispheresProcessing.RightHemisphere.GreyWhiteMesh.setSelected(
            True)
        enode.HemispheresProcessing.RightHemisphere.SulciSkeleton.setSelected(
            True)
        enode.HemispheresProcessing.RightHemisphere.PialMesh.setSelected(True)
        enode.HemispheresProcessing.RightHemisphere.CorticalFoldsGraph.setSelected(
            True)
        enode.HemispheresProcessing.RightHemisphere.SulciRecognition.setSelected(
            True)

    if self.use_morphologist == 0:
        pv = mainThreadActions().call(ProcessView, morphologist)
        mainThreadActions().call(pv.hide)
        mainThreadActions().call(pv.show)
        r = context.ask('run the pipeline, then click here', 'OK')
        # print('***************** OK clicked')
        mainThreadActions().call(pv.close)
        lock = threading.Lock()
        lock.acquire()
        mainThreadActions().push(delInMainThread, lock, pv)
        del pv
        # print('*** DELETED')
        lock.release()
        # print('lock released')
    elif self.use_morphologist == 1:
        context.runProcess(morphologist)
    else:
        context.write('<font color="#a0a060">'
                      + _t_('Pipeline not run since the "use_morphologist" parameter '
                            'prevents it') + '</font>')

    context.write('OK')
