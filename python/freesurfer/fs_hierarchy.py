
from brainvisa.data.ontology.base import *


# snapshots snapbase freesurfer
snap_aimspial_content = lambda: (
    "snapshot_freesurfer_left_aimspial_{subject}", SetType(
        'Snapshot Pial Mesh'), SetWeakAttr('side', 'left', 'processing', 'freesurfer'),
  "snapshot_freesurfer_right_aimspial_{subject}", SetType(
      'Snapshot Pial Mesh'), SetWeakAttr('side', 'right', 'processing', 'freesurfer'),
)
snap_aimswhite_content = lambda: (
    "snapshot_freesurfer_left_aimswhite_{subject}", SetType(
        'Snapshot White Mesh'), SetWeakAttr('side', 'left', 'processing', 'freesurfer'),
  "snapshot_freesurfer_right_aimswhite_{subject}", SetType(
      'Snapshot White Mesh'), SetWeakAttr('side', 'right', 'processing', 'freesurfer'),
)
snap_thickness_content = lambda: (
    "snapshot_freesurfer_left_thickness_{subject}", SetType(
        'Snapshot Thickness Map'), SetWeakAttr('side', 'left', 'processing', 'freesurfer'),
  "snapshot_freesurfer_right_thickness_{subject}", SetType(
      'Snapshot Thickness Map'), SetWeakAttr('side', 'right', 'processing', 'freesurfer'),
)
snap_gyri_content = lambda: (
    "snapshot_freesurfer_left_gyri_{subject}", SetType(
        'Snapshot Gyral Parcellation'), SetWeakAttr('side', 'left', 'processing', 'freesurfer'),
  "snapshot_freesurfer_right_gyri_{subject}", SetType(
      'Snapshot Gyral Parcellation'), SetWeakAttr('side', 'right', 'processing', 'freesurfer'),
)
snap_curv_content = lambda: (
    "snapshot_freesurfer_left_curv_{subject}", SetType(
        'Snapshot Curvature Map'), SetWeakAttr('side', 'left', 'processing', 'freesurfer'),
  "snapshot_freesurfer_right_curv_{subject}", SetType(
      'Snapshot Curvature Map'), SetWeakAttr('side', 'right', 'processing', 'freesurfer'),
)


fs_snapshots = lambda: (
    'freesurfer', SetContent(
        'greywhite', SetContent(
            'snapshot_freesurfer_greywhite_{subject}', SetType(
                'Snapshot Grey White'), SetWeakAttr('processing', 'freesurfer'),
            'qc_greywhite', SetType('Snapshots Grey White Quality Scores'), SetWeakAttr(
                'processing', 'freesurfer'),
        ),
        'meshcut', SetContent(
            'snapshot_freesurfer_meshcut_{subject}', SetType(
                'Snapshot Meshcut'), SetWeakAttr('processing', 'freesurfer'),
        ),
        'aimspial', SetContent(*snap_aimspial_content()),
        'aimswhite', SetContent(*snap_aimswhite_content()),
        'thickness', SetContent(*snap_thickness_content()),
        'gyri', SetContent(*snap_gyri_content()),
        'curv', SetContent(*snap_curv_content()),
    ),
)


fs_tables = lambda: (
    'thicknesses_freesurfer', SetType(
        'Cortical Thicknesses Table'), SetWeakAttr('processing', 'freesurfer'),
    'tissues_volumes_freesurfer', SetType(
        'Global Volumetry Table'), SetWeakAttr('processing', 'freesurfer'),
    'history_thicknesses_freesurfer', SetType(
        'History Cortical Thicknesses Table'), SetWeakAttr('processing', 'freesurfer'),
    'history_tissues_volumes_freesurfer', SetType(
        'History Global Volumetry Table'), SetWeakAttr('processing', 'freesurfer'),
    'snapshots_features_freesurfer', SetType(
        'Snapshots Features Table'), SetWeakAttr('processing', 'freesurfer'),
)


fs_group_analysis = lambda: (
    '<freesurfer_group_of_subjects>_group',
    SetType('Freesurfer Group definition'),
    'average_brain', SetContent(
        'lh.averagebrain.white', SetType('AverageBrainWhite'),
        SetWeakAttr(
            'side', 'left', 'averaged', 'Yes', 'inflated', 'No',
            'vertex_corr', 'Yes',
            'vertex_corr_method', 'freesurfer'),
        'rh.averagebrain.white', SetType('AverageBrainWhite'),
        SetWeakAttr(
            'side', 'right', 'averaged', 'Yes', 'inflated', 'No',
            'vertex_corr', 'Yes',
            'vertex_corr_method', 'freesurfer'),
        'averagebrain.white', SetType('BothAverageBrainWhite'),
        SetWeakAttr(
            'side', 'both', 'averaged', 'Yes', 'inflated', 'No',
            'vertex_corr', 'Yes',
            'vertex_corr_method', 'freesurfer'),
        'averagebrain.white.inflated', SetType(
            'BothAverageBrainWhite'),
        SetWeakAttr(
            'side', 'both', 'averaged', 'Yes', 'inflated', 'Yes',
            'vertex_corr', 'Yes',
            'vertex_corr_method', 'freesurfer'),
        'bh.annot.averagebrain', SetType('BothAverageResampledGyri'),
        SetWeakAttr(
            'side', 'both', 'averaged', 'Yes', 'vertex_corr', 'Yes',
              'vertex_corr_method', 'freesurfer'),
    ),
)


fs_subject = lambda: (
    'mri', SetContent(
        'orig', SetType('T1 FreesurferAnat'),
        'nu', SetType('Nu FreesurferAnat'),
        'brainmask', SetType('Freesurfer Brain Mask'),
        'ribbon', SetType('Ribbon Freesurfer'),
        SetWeakAttr('side', 'both',
                    'space', 'freesurfer analysis'),
        'ribbon_native', SetType('Ribbon Freesurfer'),
        SetWeakAttr('side', 'both',
                    'space', 'native'),
        'lh.ribbon', SetType('Ribbon Freesurfer'),
        SetWeakAttr('side', 'left',
                    'space', 'freesurfer analysis'),
        'lh.ribbon_native', SetType('Ribbon Freesurfer'),
        SetWeakAttr('side', 'left',
                    'space', 'native'),
        'rh.ribbon', SetType('Ribbon Freesurfer'),
        SetWeakAttr('side', 'right',
                    'space', 'freesurfer analysis'),
        'rh.ribbon_native', SetType('Ribbon Freesurfer'),
        SetWeakAttr('side', 'right',
                    'space', 'native'),
        'aseg', SetType('Freesurfer aseg'),
        SetWeakAttr('space', 'freesurfer analysis'),
        'aseg_native', SetType('Freesurfer aseg'),
        SetWeakAttr('space', 'native'),
        'aparc+aseg', SetType('Freesurfer Cortical Parcellation'),
        SetWeakAttr('atlas', 'Desikan-Killiany',
                    'space', 'freesurfer analysis'),
        'aparc+aseg_native', SetType('Freesurfer Cortical Parcellation'),
        SetWeakAttr('atlas', 'Desikan-Killiany',
                    'space', 'native'),
        'aparc.a2009s+aseg', SetType('Freesurfer Cortical Parcellation'),
        SetWeakAttr('atlas', 'Destrieux',
                    'space', 'freesurfer analysis'),
        'aparc.a2009s+aseg_native', SetType(
            'Freesurfer Cortical Parcellation'),
        SetWeakAttr('atlas', 'Destrieux',
                    'space', 'native'),
        'transforms', SetContent(
            'talairach.auto', SetType('Talairach Auto Freesurfer'),
            'orig_<subject>_TO_Scanner_Based', SetType(
                'Transformation to Scanner Based Referential'),
            'orig_<subject>_Scanner_Based', SetType(
                'Scanner Based Referential'),
            '<subject>_meshes', SetType('Referential of Pial'),
            '<subject>_orig_TO_meshes', SetType(
                'Freesurfer Anat To Meshes Transformation'),
            '<subject>_scanner_to_mni', SetType(
                'Freesurfer Scanner To MNI Transformation'),
        ),
        'orig', SetContent(
            '001', SetType('RawFreesurferAnat'),
            '001', SetType('Referential of Raw T1 MRI'),
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
        'lh.sphere.reg', SetType(
            'SphereReg'), SetWeakAttr('side', 'left'),
        'rh.sphere.reg', SetType(
            'SphereReg'), SetWeakAttr('side', 'right'),
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
        SetPriorityOffset(10),  # higher priority than inflated version
        'rh.r.aims.white', SetType('AimsWhite'),
        SetWeakAttr('side', 'right', 'averaged', 'No', 'inflated', 'No',
                    'vertex_corr', 'Yes',
                    'vertex_corr_method', 'freesurfer'),
        SetPriorityOffset(10),  # higher priority than inflated version
        'lh.aims.pial', SetType('AimsNativePial'),
        SetWeakAttr('side', 'left', 'averaged', 'No', 'inflated', 'No',
                    'vertex_corr', 'No'),
        'rh.aims.pial', SetType('AimsNativePial'),
        SetWeakAttr('side', 'right', 'averaged', 'No', 'inflated', 'No',
                    'vertex_corr', 'No'),
        'lh.aims.white', SetType('AimsNativeWhite'),
        SetWeakAttr('side', 'left', 'averaged', 'No', 'inflated', 'No',
                    'vertex_corr', 'No'),
        'rh.aims.white', SetType('AimsNativeWhite'),
        SetWeakAttr('side', 'right', 'averaged', 'No', 'inflated', 'No',
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
                    'vertex_corr_method', 'freesurfer',
                    'time_sequence', 'No'),
        'bh.r.aims.white.inflated_sequence', SetType(
            'AimsBothInflatedWhite'),
        SetPriorityOffset(-10),
        SetWeakAttr('side', 'both', 'averaged', 'No', 'inflated', 'Yes',
                    'vertex_corr', 'Yes',
                    'vertex_corr_method', 'freesurfer',
                    'time_sequence', 'Yes'),
        #
        'lh.r.aims.white.inflated', SetType('AimsInflatedWhite'),
        SetWeakAttr('side', 'left', 'averaged', 'No', 'inflated', 'Yes',
                    'vertex_corr', 'Yes',
                    'vertex_corr_method', 'freesurfer',
                    'time_sequence', 'No'),
        'rh.r.aims.white.inflated', SetType('AimsInflatedWhite'),
        SetWeakAttr('side', 'right', 'averaged', 'No', 'inflated', 'Yes',
                    'vertex_corr', 'Yes',
                    'vertex_corr_method', 'freesurfer',
                    'time_sequence', 'No'),
        'lh.r.aims.white.inflated_sequence', SetType(
            'AimsInflatedWhite'),
        SetPriorityOffset(-10),
        SetWeakAttr('side', 'left', 'averaged', 'No', 'inflated', 'Yes',
                    'vertex_corr', 'Yes',
                    'vertex_corr_method', 'freesurfer',
                    'time_sequence', 'Yes'),
        'rh.r.aims.white.inflated_sequence', SetType(
            'AimsInflatedWhite'),
        SetPriorityOffset(-10),
        SetWeakAttr('side', 'right', 'averaged', 'No', 'inflated', 'Yes',
                    'vertex_corr', 'Yes',
                    'vertex_corr_method', 'freesurfer',
                    'time_sequence', 'Yes'),
        'lh.r.curv.white.inflated', SetType('AimsInflatedWhiteCurvTex'),
        SetWeakAttr('side', 'left', 'averaged', 'No',
                    'vertex_corr', 'Yes',
                    'vertex_corr_method', 'freesurfer'),
        # FIXME: why is the curvature (texture) "inflated" ?
        'rh.r.curv.white.inflated', SetType('AimsInflatedWhiteCurvTex'),
        SetWeakAttr(
            'side', 'right', 'averaged', 'No', 'vertex_corr', 'Yes',
                'vertex_corr_method', 'freesurfer'),
        #
        'lh.avg_curv', SetType('FreesurferAvgCurvType'),
        SetWeakAttr(
            'side', 'left', 'averaged', 'No', 'vertex_corr', 'No'),
        'rh.avg_curv', SetType('FreesurferAvgCurvType'),
        SetWeakAttr(
            'side', 'right', 'averaged', 'No', 'vertex_corr', 'No'),
        'lh.curv.pial', SetType('FreesurferCurvPialType'),
        SetWeakAttr(
            'side', 'left', 'averaged', 'No', 'vertex_corr', 'No'),
        'rh.curv.pial', SetType('FreesurferCurvPialType'),
        SetWeakAttr(
            'side', 'right', 'averaged', 'No', 'vertex_corr', 'No'),
        'lh.curv', SetType('FreesurferCurvType'),
        SetWeakAttr(
            'side', 'left', 'averaged', 'No', 'vertex_corr', 'No'),
        'rh.curv', SetType('FreesurferCurvType'),
        SetWeakAttr(
            'side', 'right', 'averaged', 'No', 'vertex_corr', 'No'),
        'lh.thickness', SetType('FreesurferThicknessType'),
        SetWeakAttr(
            'side', 'left', 'averaged', 'No', 'vertex_corr', 'No'),
        'rh.thickness', SetType('FreesurferThicknessType'),
        SetWeakAttr(
            'side', 'right', 'averaged', 'No', 'vertex_corr', 'No'),
        #
        'lh.r.avg_curv', SetType('ResampledFreesurferAvgCurvType'),
        SetWeakAttr(
            'side', 'left', 'averaged', 'No', 'vertex_corr', 'Yes',
                'vertex_corr_method', 'freesurfer'),
        'rh.r.avg_curv', SetType('ResampledFreesurferAvgCurvType'),
        SetWeakAttr(
            'side', 'right', 'averaged', 'No', 'vertex_corr', 'Yes',
                'vertex_corr_method', 'freesurfer'),
        'lh.r.curv.pial', SetType('ResampledFreesurferCurvPialType'),
        SetWeakAttr(
            'side', 'left', 'averaged', 'No', 'vertex_corr', 'Yes',
                'vertex_corr_method', 'freesurfer'),
        'rh.r.curv.pial', SetType('ResampledFreesurferCurvPialType'),
        SetWeakAttr(
            'side', 'right', 'averaged', 'No', 'vertex_corr', 'Yes',
                'vertex_corr_method', 'freesurfer'),
        'lh.r.curv', SetType('ResampledFreesurferCurvType'),
        SetWeakAttr(
            'side', 'left', 'averaged', 'No', 'vertex_corr', 'Yes',
                'vertex_corr_method', 'freesurfer'),
        'rh.r.curv', SetType('ResampledFreesurferCurvType'),
        SetWeakAttr(
            'side', 'right', 'averaged', 'No', 'vertex_corr', 'Yes',
                'vertex_corr_method', 'freesurfer'),
        'lh.r.thickness', SetType('ResampledFreesurferThicknessType'),
        SetWeakAttr(
            'side', 'left', 'averaged', 'No', 'vertex_corr', 'Yes',
                'vertex_corr_method', 'freesurfer'),
        'rh.r.thickness', SetType('ResampledFreesurferThicknessType'),
        SetWeakAttr(
            'side', 'right', 'averaged', 'No', 'vertex_corr', 'Yes',
                'vertex_corr_method', 'freesurfer'),
        #
        'lh', SetType('BaseFreesurferType'), SetWeakAttr('side', 'left'),
        'rh', SetType('BaseFreesurferType'), SetWeakAttr(
            'side', 'right'),
    ),
    'label', SetType('FreesurferParcellationPath'), SetContent(
        'lh.aparc', SetType('FreesurferGyriTexture'),
        SetWeakAttr(
            'side', 'left', 'averaged', 'No', 'vertex_corr', 'No'),
        'rh.aparc', SetType('FreesurferGyriTexture'),
        SetWeakAttr(
            'side', 'right', 'averaged', 'No', 'vertex_corr', 'No'),
        'lh.aparc.a2009s', SetType('FreesurferSulciGyriTexture'),
        SetWeakAttr(
            'side', 'left', 'averaged', 'No', 'vertex_corr', 'No'),
        'rh.aparc.a2009s', SetType('FreesurferSulciGyriTexture'),
        SetWeakAttr(
            'side', 'right', 'averaged', 'No', 'vertex_corr', 'No'),
        # 'lh.aparc.annot-#', SetType('FreesurferReadableGyriTexture'),
        # SetWeakAttr('side', 'left', 'averaged', 'No', 'vertex_corr', 'No'),
        # 'rh.aparc.annot-#', SetType('FreesurferReadableGyriTexture'),
        # SetWeakAttr('side', 'right', 'averaged', 'No', 'vertex_corr', 'No'),
        # 'lh.aparc.a2009s.annot-#',
        # SetType('FreesurferReadableSulciGyriTexture'),
        # SetWeakAttr('side', 'left', 'averaged', 'No', 'vertex_corr', 'No'),
        # 'rh.aparc.a2009s.annot-#',
        # SetType('FreesurferReadableSulciGyriTexture'),
        # SetWeakAttr('side', 'right', 'averaged', 'No', 'vertex_corr',
        # 'No'),
        'lh.aparc.annot', SetType('FreesurferGyri'),
        SetWeakAttr(
            'side', 'left', 'averaged', 'No', 'vertex_corr', 'No'),
        'rh.aparc.annot', SetType('FreesurferGyri'),
        SetWeakAttr(
            'side', 'right', 'averaged', 'No', 'vertex_corr', 'No'),
        'lh.aparc.a2009s.annot', SetType('FreesurferSulciGyri'),
        SetWeakAttr(
            'side', 'left', 'averaged', 'No', 'vertex_corr', 'No'),
        'rh.aparc.a2009s.annot', SetType('FreesurferSulciGyri'),
        SetWeakAttr(
            'side', 'right', 'averaged', 'No', 'vertex_corr', 'No'),
        #
        'lh.r.aparc.annot', SetType('ResampledGyri'),
        SetWeakAttr(
            'side', 'left', 'averaged', 'No', 'vertex_corr', 'Yes',
                'vertex_corr_method', 'freesurfer'),
        'rh.r.aparc.annot', SetType('ResampledGyri'),
        SetWeakAttr(
            'side', 'right', 'averaged', 'No', 'vertex_corr', 'Yes',
                'vertex_corr_method', 'freesurfer'),
        'lh.r.aparc.a2009s.annot', SetType('ResampledSulciGyri'),
        SetWeakAttr(
            'side', 'left', 'averaged', 'No', 'vertex_corr', 'Yes',
                'vertex_corr_method', 'freesurfer'),
        'rh.r.aparc.a2009s.annot', SetType('ResampledSulciGyri'),
        SetWeakAttr(
            'side', 'right', 'averaged', 'No', 'vertex_corr', 'Yes',
                'vertex_corr_method', 'freesurfer'),
        #
        'bh.r.aparc.annot', SetType('BothResampledGyri'),
        SetWeakAttr(
            'side', 'both', 'averaged', 'No', 'vertex_corr', 'Yes',
                'vertex_corr_method', 'freesurfer'),
        'bh.r.aparc.a2009s.annot', SetType('BothResampledSulciGyri'),
        SetWeakAttr(
            'side', 'both', 'averaged', 'No', 'vertex_corr', 'Yes',
                'vertex_corr_method', 'freesurfer'),
    ),
)

