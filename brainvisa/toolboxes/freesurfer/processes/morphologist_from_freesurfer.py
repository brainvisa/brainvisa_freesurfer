
from brainvisa.processing import capsul_process
from brainvisa.processes import Signature, ReadDiskItem, WriteDiskItem

name = 'Morphologist from Freesurfer'
userLevel = 2  # completion is not fully working

base_class = capsul_process.CapsulProcess
capsul_process = 'brainvisa.freesurfer.capsul.morphologist_from_freesurfer'

signature = Signature(
    'T1_orig', ReadDiskItem('T1 FreesurferAnat',
                            'FreesurferMGZ',
                            exactType=True),
    'ribbon_image', ReadDiskItem(
        'Ribbon Freesurfer',
        'FreesurferMGZ',
        requiredAttributes={'side': 'both', 'space': 'freesurfer analysis'}),
    'scanner_based_referential', ReadDiskItem('Scanner Based Referential',
                                              'Referential'),
    'Talairach_Auto', ReadDiskItem('Talairach Auto Freesurfer',
                                   'MINC transformation matrix'),
    'imported_t1mri', WriteDiskItem('Raw T1 MRI',
                                    ['gz compressed NIFTI-1 image',
                                     'NIFTI-1 image',
                                     'GIS image']),
    't1mri_referential', WriteDiskItem('Referential of Raw T1 MRI',
                                       'Referential'),
    'transform_to_scanner_based', WriteDiskItem(
        'Transformation to Scanner Based Referential',
        'Transformation matrix'),
    't1mri_nobias', WriteDiskItem('T1 MRI Bias Corrected',
                                  'Aims writable volume formats'),
    'MNI_transform', WriteDiskItem(
        'Transform Raw T1 MRI to Talairach-MNI template-SPM',
        'Transformation matrix'),
    'talairach_transform', WriteDiskItem(
        'Transform Raw T1 MRI to Talairach-AC/PC-Anatomist',
        'Transformation matrix'),
    'commissure_coordinates', WriteDiskItem('Commissure Coordinates',
                                            'Commissure coordinates'),
    'histo_analysis', WriteDiskItem('Histo Analysis',
                                    'Histo Analysis'),
    'BrainSegmentation_brain_mask', WriteDiskItem(
        'T1 Brain Mask', 'Aims writable volume formats'),
    'split_brain', WriteDiskItem('Split Brain Mask',
                                 'Aims writable volume formats'),
    'GreyWhiteClassification_grey_white', WriteDiskItem(
        'Left Grey White Mask', 'Aims writable volume formats'),
    'GreyWhiteClassification_1_grey_white', WriteDiskItem(
        'Right Grey White Mask', 'Aims writable volume formats'),
    'mni_referential', ReadDiskItem('Referential', 'Referential'),
    'transform_chain_ACPC_to_Normalized', ReadDiskItem(
        'Transformation', 'Transformation matrix'),
    'acpc_referential', ReadDiskItem('Referential', 'Referential'),
)
