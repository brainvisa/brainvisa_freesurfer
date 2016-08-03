# -*- coding: utf-8 -*-
# Copyright CEA and IFR 49 (2000-2005)
#
#  This software and supporting documentation were developed by
#      CEA/DSV/SHFJ and IFR 49
#      4 place du General Leclerc
#      91401 Orsay cedex
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


#snapshots snapbase freesurfer
snap_aimspial_content = (
  "snapshot_freesurfer_left_aimspial_{subject}", SetType( 'Snapshot Pial Mesh'), SetWeakAttr( 'side', 'left', 'processing', 'freesurfer'  ),
  "snapshot_freesurfer_right_aimspial_{subject}", SetType( 'Snapshot Pial Mesh'), SetWeakAttr( 'side', 'right', 'processing', 'freesurfer'  ),
)
snap_aimswhite_content = (
  "snapshot_freesurfer_left_aimswhite_{subject}", SetType( 'Snapshot White Mesh'), SetWeakAttr( 'side', 'left', 'processing', 'freesurfer'  ),
  "snapshot_freesurfer_right_aimswhite_{subject}", SetType( 'Snapshot White Mesh'), SetWeakAttr( 'side', 'right', 'processing', 'freesurfer'  ),
)
snap_thickness_content = (
  "snapshot_freesurfer_left_thickness_{subject}", SetType( 'Snapshot Thickness Map'), SetWeakAttr( 'side', 'left', 'processing', 'freesurfer'  ),
  "snapshot_freesurfer_right_thickness_{subject}", SetType( 'Snapshot Thickness Map'), SetWeakAttr( 'side', 'right', 'processing', 'freesurfer'  ),
)
snap_gyri_content = (
  "snapshot_freesurfer_left_gyri_{subject}", SetType( 'Snapshot Gyral Parcellation'), SetWeakAttr( 'side', 'left', 'processing', 'freesurfer'  ),
  "snapshot_freesurfer_right_gyri_{subject}", SetType( 'Snapshot Gyral Parcellation'), SetWeakAttr( 'side', 'right', 'processing', 'freesurfer'  ),
)
snap_curv_content = (
  "snapshot_freesurfer_left_curv_{subject}", SetType( 'Snapshot Curvature Map'), SetWeakAttr( 'side', 'left', 'processing', 'freesurfer'  ),
  "snapshot_freesurfer_right_curv_{subject}", SetType( 'Snapshot Curvature Map'), SetWeakAttr( 'side', 'right', 'processing', 'freesurfer'  ),
)

hierarchy = (
  SetWeakAttr( 'database', '%f' ),
  SetContent(
    'snapshots',SetContent(
      'freesurfer', SetContent(
        'greywhite', SetContent(
        "snapshot_freesurfer_greywhite_{subject}", SetType( 'Snapshot Grey White'), SetWeakAttr('processing', 'freesurfer'),
        "qc_greywhite", SetType( 'Snapshots Grey White Quality Scores') , SetWeakAttr('processing', 'freesurfer'),
         ),
        'aimspial', apply(SetContent,snap_aimspial_content),
        'aimswhite', apply(SetContent, snap_aimswhite_content),
        'thickness', apply(SetContent, snap_thickness_content),
        'gyri', apply(SetContent, snap_gyri_content),
        'curv', apply(SetContent, snap_curv_content),
        ),
      ),
    'tables',SetContent(
        'thicknesses_freesurfer', SetType('Cortical Thicknesses Table'), SetWeakAttr('processing', 'freesurfer'),
        'tissues_volumes_freesurfer', SetType('Global Volumetry Table'), SetWeakAttr('processing', 'freesurfer'),
        'history_thicknesses_freesurfer', SetType('History Cortical Thicknesses Table'), SetWeakAttr('processing', 'freesurfer'),
        'history_tissues_volumes_freesurfer', SetType('History Global Volumetry Table'), SetWeakAttr('processing', 'freesurfer'),    
        'snapshots_features_freesurfer', SetType('Snapshots Features Table'), SetWeakAttr('processing', 'freesurfer'),
      ),
    'history_book', SetContent(
    'bvsession', SetType( 'Bvsession' ),
    SetContent('*', SetType( 'BrainVISA session event' ),),
    '*', SetContent('*', SetType( 'Process execution event' ),),
    ),
    'database_fso', SetType( 'Database description page' ),
    'database_settings', SetType( 'Database settings' ),
    'snapshots', SetType('Snapshots Dir'), SetContent(),
    'tables', SetType('Tables Directory'), SetContent(),
    '*', SetType('Database Cache file'),
        'group_analysis',
    SetContent(
    '{freesurfer_group_of_subjects}',
    SetContent(
      '<freesurfer_group_of_subjects>_group',
        SetType( 'Freesurfer Group definition' ),
      'average_brain', SetContent(
        'lh.averagebrain.white', SetType('AverageBrainWhite'),
          SetWeakAttr('side', 'left', 'averaged', 'Yes', 'inflated', 'No',
                      'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'rh.averagebrain.white', SetType('AverageBrainWhite'),
          SetWeakAttr('side','right', 'averaged', 'Yes', 'inflated', 'No',
                      'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'averagebrain.white', SetType('BothAverageBrainWhite'),
          SetWeakAttr('side', 'both', 'averaged', 'Yes', 'inflated', 'No',
                      'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'bh.annot.averagebrain', SetType('BothAverageResampledGyri'),
          SetWeakAttr('side', 'both', 'averaged', 'Yes', 'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
    ))),
    '{subject}', SetFileNameStrongAttribute('subject'), SetType('Subject'),
    SetContent(
      'mri', SetContent(
        'orig', SetType( 'T1 FreesurferAnat' ),
        'nu', SetType( 'Nu FreesurferAnat' ),
        'ribbon', SetType( 'Ribbon Freesurfer' ),
        'aseg', SetType( 'Freesurfer aseg' ),
        'aparc.a2009s+aseg', SetType( 'Freesurfer Cortical Parcellation using Destrieux Atlas' ),
        'brainmask', SetType( 'Freesurfer Brain Mask' ),
        'transforms', SetContent(
          'talairach.auto', SetType('Talairach Auto Freesurfer'),
          'orig_<subject>_TO_Scanner_Based', SetType( 'Transformation to Scanner Based Referential' ),
          'orig_<subject>_Scanner_Based', SetType( 'Scanner Based Referential' ),
          '<subject>_meshes', SetType( 'Referential of Pial' ),
          '<subject>_orig_TO_meshes', SetType( 'Freesurfer Anat To Meshes Transformation' ),
          '<subject>_scanner_to_mni', SetType( 'Freesurfer Scanner To MNI Transformation' ),
       ),
        'orig', SetContent(
          '001', SetType('RawFreesurferAnat'),
          '001', SetType( 'Referential of Raw T1 MRI' ),
        ),
      ),
      'surf', SetContent(
        'lh.pial', SetType('Pial'),
          SetWeakAttr('side', 'left', 'averaged', 'No', 'inflated', 'No',
                      'vertex_corr', 'No'),
        'rh.pial', SetType('Pial'),
          SetWeakAttr('side', 'right', 'averaged', 'No', 'inflated', 'No',
                      'vertex_corr', 'No'),
        'lh.white', SetType('White'),
          SetWeakAttr('side', 'left', 'averaged', 'No', 'inflated', 'No',
                      'vertex_corr', 'No'),
        'rh.white', SetType('White'),
          SetWeakAttr('side', 'right', 'averaged', 'No', 'inflated', 'No',
                      'vertex_corr', 'No'),
        'lh.sphere.reg', SetType('SphereReg'), SetWeakAttr('side','left'),
        'rh.sphere.reg', SetType('SphereReg'), SetWeakAttr('side','right'),
        #
        'lh.r.pial', SetType('ResampledPial'),
          SetWeakAttr('side', 'left', 'averaged', 'No', 'inflated', 'No',
                      'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'rh.r.pial', SetType('ResampledPial'),
          SetWeakAttr('side', 'right', 'averaged', 'No', 'inflated', 'No',
                      'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'lh.r.white', SetType('ResampledWhite'),
          SetWeakAttr('side', 'left', 'averaged', 'No', 'inflated', 'No',
                      'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'rh.r.white', SetType('ResampledWhite'),
          SetWeakAttr('side', 'right', 'averaged', 'No', 'inflated', 'No',
                      'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'lh.r.aims.pial', SetType('AimsPial'),
          SetWeakAttr('side', 'left', 'averaged', 'No', 'inflated', 'No',
                      'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'rh.r.aims.pial', SetType('AimsPial'),
          SetWeakAttr('side', 'right', 'averaged', 'No', 'inflated', 'No',
                      'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'lh.r.aims.white', SetType('AimsWhite'),
          SetWeakAttr('side', 'left', 'averaged', 'No', 'inflated', 'No',
                      'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
          SetPriorityOffset(10), # higher priority than inflated version
        'rh.r.aims.white', SetType('AimsWhite'),
          SetWeakAttr('side', 'right', 'averaged', 'No', 'inflated', 'No',
                      'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
          SetPriorityOffset(10), # higher priority than inflated version
        'lh.aims.pial', SetType('AimsNativePial'),
          SetWeakAttr('side', 'left', 'averaged', 'No', 'inflated', 'No',
                      'vertex_corr', 'No'),
        'rh.aims.pial', SetType('AimsNativePial'),
          SetWeakAttr('side','right', 'averaged', 'No', 'inflated', 'No',
                      'vertex_corr', 'No'),
        'lh.aims.white', SetType('AimsNativeWhite'),
          SetWeakAttr('side','left', 'averaged', 'No', 'inflated', 'No',
                      'vertex_corr', 'No'),
        'rh.aims.white', SetType('AimsNativeWhite'),
          SetWeakAttr('side','right', 'averaged', 'No', 'inflated', 'No',
                      'vertex_corr', 'No'),
        #
        'lh.r.aims.white.normalized', SetType('AimsNormalizedWhite'),
          SetWeakAttr('side', 'left', 'averaged', 'No', 'inflated', 'No',
                      'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'rh.r.aims.white.normalized', SetType('AimsNormalizedWhite'),
          SetWeakAttr('side', 'right', 'averaged', 'No', 'inflated', 'No',
                      'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        #
        'bh.r.aims.white', SetType('AimsBothWhite'),
          SetWeakAttr('side', 'both', 'averaged', 'No', 'inflated', 'No',
                      'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'bh.r.aims.pial', SetType('AimsBothPial'),
          SetWeakAttr('side', 'both', 'averaged', 'No', 'inflated', 'No',
                      'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'bh.r.aims.white.inflated', SetType('AimsBothInflatedWhite'),
          SetWeakAttr('side', 'both', 'averaged', 'No', 'inflated', 'Yes',
                      'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        #
        'lh.r.aims.white.inflated', SetType('AimsInflatedWhite'),
          SetWeakAttr('side', 'left', 'averaged', 'No', 'inflated', 'Yes',
                      'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'rh.r.aims.white.inflated', SetType('AimsInflatedWhite'),
          SetWeakAttr('side', 'right', 'averaged', 'No', 'inflated', 'Yes',
                      'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'lh.r.curv.white.inflated', SetType('AimsInflatedWhiteCurvTex'),
          SetWeakAttr('side', 'left', 'averaged', 'No',
                      'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        # FIXME: why is the curvature (texture) "inflated" ?
        'rh.r.curv.white.inflated', SetType('AimsInflatedWhiteCurvTex'),
          SetWeakAttr('side', 'right', 'averaged', 'No', 'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        #
        'lh.avg_curv', SetType('FreesurferAvgCurvType'),
          SetWeakAttr('side', 'left', 'averaged', 'No', 'vertex_corr', 'No'),
        'rh.avg_curv', SetType('FreesurferAvgCurvType'),
          SetWeakAttr('side', 'right', 'averaged', 'No', 'vertex_corr', 'No'),
        'lh.curv.pial', SetType('FreesurferCurvPialType'),
          SetWeakAttr('side', 'left', 'averaged', 'No', 'vertex_corr', 'No'),
        'rh.curv.pial', SetType('FreesurferCurvPialType'),
          SetWeakAttr('side', 'right', 'averaged', 'No', 'vertex_corr', 'No'),
        'lh.curv', SetType('FreesurferCurvType'),
          SetWeakAttr('side', 'left', 'averaged', 'No', 'vertex_corr', 'No'),
        'rh.curv', SetType('FreesurferCurvType'),
          SetWeakAttr('side', 'right', 'averaged', 'No', 'vertex_corr', 'No'),
        'lh.thickness', SetType('FreesurferThicknessType'),
          SetWeakAttr('side', 'left', 'averaged', 'No', 'vertex_corr', 'No'),
        'rh.thickness', SetType('FreesurferThicknessType'),
          SetWeakAttr('side', 'right', 'averaged', 'No', 'vertex_corr', 'No'),
        #
        'lh.r.avg_curv', SetType('ResampledFreesurferAvgCurvType'),
          SetWeakAttr('side', 'left', 'averaged', 'No', 'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'rh.r.avg_curv', SetType('ResampledFreesurferAvgCurvType'),
          SetWeakAttr('side', 'right', 'averaged', 'No', 'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'lh.r.curv.pial', SetType('ResampledFreesurferCurvPialType'),
          SetWeakAttr('side', 'left', 'averaged', 'No', 'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'rh.r.curv.pial', SetType('ResampledFreesurferCurvPialType'),
          SetWeakAttr('side', 'right', 'averaged', 'No', 'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'lh.r.curv', SetType('ResampledFreesurferCurvType'),
          SetWeakAttr('side', 'left', 'averaged', 'No', 'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'rh.r.curv', SetType('ResampledFreesurferCurvType'),
          SetWeakAttr('side', 'right', 'averaged', 'No', 'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'lh.r.thickness', SetType('ResampledFreesurferThicknessType'),
          SetWeakAttr('side', 'left', 'averaged', 'No', 'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'rh.r.thickness', SetType('ResampledFreesurferThicknessType'),
          SetWeakAttr('side', 'right', 'averaged', 'No', 'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        #
        'lh', SetType('BaseFreesurferType'), SetWeakAttr('side','left'),
        'rh', SetType('BaseFreesurferType'), SetWeakAttr('side','right'),
      ),
      'label', SetType('FreesurferParcellationPath'), SetContent(
        'lh.aparc', SetType('FreesurferGyriTexture'),
          SetWeakAttr('side', 'left', 'averaged', 'No', 'vertex_corr', 'No'),
        'rh.aparc', SetType('FreesurferGyriTexture'),
          SetWeakAttr('side', 'right', 'averaged', 'No', 'vertex_corr', 'No'),
        'lh.aparc.a2009s', SetType('FreesurferSulciGyriTexture'),
          SetWeakAttr('side', 'left', 'averaged', 'No', 'vertex_corr', 'No'),
        'rh.aparc.a2009s', SetType('FreesurferSulciGyriTexture'),
          SetWeakAttr('side', 'right', 'averaged', 'No', 'vertex_corr', 'No'),
        #'lh.aparc.annot-#', SetType('FreesurferReadableGyriTexture'),
          #SetWeakAttr('side', 'left', 'averaged', 'No', 'vertex_corr', 'No'),
        #'rh.aparc.annot-#', SetType('FreesurferReadableGyriTexture'),
          #SetWeakAttr('side', 'right', 'averaged', 'No', 'vertex_corr', 'No'),
        #'lh.aparc.a2009s.annot-#',
          #SetType('FreesurferReadableSulciGyriTexture'),
          #SetWeakAttr('side', 'left', 'averaged', 'No', 'vertex_corr', 'No'),
        #'rh.aparc.a2009s.annot-#',
          #SetType('FreesurferReadableSulciGyriTexture'),
          #SetWeakAttr('side', 'right', 'averaged', 'No', 'vertex_corr', 'No'),
        'lh.aparc.annot', SetType('FreesurferGyri'),
          SetWeakAttr('side', 'left', 'averaged', 'No', 'vertex_corr', 'No'),
        'rh.aparc.annot', SetType('FreesurferGyri'),
          SetWeakAttr('side', 'right', 'averaged', 'No', 'vertex_corr', 'No'),
        'lh.aparc.a2009s.annot', SetType('FreesurferSulciGyri'),
          SetWeakAttr('side', 'left', 'averaged', 'No', 'vertex_corr', 'No'),
        'rh.aparc.a2009s.annot', SetType('FreesurferSulciGyri'),
          SetWeakAttr('side', 'right', 'averaged', 'No', 'vertex_corr', 'No'),
        #
        'lh.r.aparc.annot', SetType('ResampledGyri'),
          SetWeakAttr('side', 'left', 'averaged', 'No', 'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'rh.r.aparc.annot', SetType('ResampledGyri'),
          SetWeakAttr('side', 'right', 'averaged', 'No', 'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'lh.r.aparc.a2009s.annot', SetType('ResampledSulciGyri'),
          SetWeakAttr('side', 'left', 'averaged', 'No', 'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'rh.r.aparc.a2009s.annot', SetType('ResampledSulciGyri'),
          SetWeakAttr('side', 'right', 'averaged', 'No', 'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        #
        'bh.r.aparc.annot', SetType('BothResampledGyri'),
          SetWeakAttr('side', 'both', 'averaged', 'No', 'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
        'bh.r.aparc.a2009s.annot', SetType('BothResampledSulciGyri'),
          SetWeakAttr('side', 'both', 'averaged', 'No', 'vertex_corr', 'Yes',
                      'vertex_corr_method', 'freesurfer'),
      ),
    ),
  ),
)
