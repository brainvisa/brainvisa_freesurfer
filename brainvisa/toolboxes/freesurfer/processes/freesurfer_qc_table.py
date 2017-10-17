
from brainvisa.processes import *

name = 'Freesurfer / BrainVISA QC table'
userLevel = 0

signature = Signature(
    'database', Choice(),
    'keys', ListOf(String()),
    'data_filters', ListOf(String()),
    'output_file', WriteDiskItem('Text File', ['HTML', 'PDF file']),
)


def initialization(self):
    # list of possible databases, while respecting the ontology
    # ontology: freesurfer
    databases = [h.name for h in neuroHierarchy.hierarchies()
                 if h.fso.name == "freesurfer"]
    self.signature["database"].setChoices(*databases)
    if len(databases) >= 1:
        self.database = databases[0]
    else:
        self.signature["database"] = OpenChoice()

    self.setOptional('data_filters', 'output_file')
    self.keys = ['subject']


def execution(self, context):
    dtypes = ['RawFreesurferAnat', 'Ribbon Freesurfer',
              'Freesurfer Scanner To MNI Transformation',
              'Pial', 'Pial', 'White', 'White',
              'AimsPial', 'AimsPial', 'AimsWhite', 'AimsWhite',
              'FreesurferGyri', 'FreesurferGyri',
              'FreesurferSulciGyri', 'FreesurferSulciGyri',
              'ResampledGyri', 'ResampledGyri',
              'ResampledSulciGyri', 'ResampledSulciGyri',
              'ResampledFreesurferCurvType', 'ResampledFreesurferCurvType',
              'ResampledFreesurferAvgCurvType',
              'ResampledFreesurferAvgCurvType',
              'ResampledFreesurferCurvPialType',
              'ResampledFreesurferCurvPialType',
              'ResampledFreesurferThicknessType',
              'ResampledFreesurferThicknessType',
              'AimsInflatedWhite', 'AimsInflatedWhite',
              'AimsBothWhite', 'AimsBothPial', 'AimsBothInflatedWhite',
              'BothResampledGyri', 'BothResampledSulciGyri']

    tlabels = ['Raw T1', 'Ribbon',
              'Freesurfer To MNI Transformation',
              'Left Pial Mesh', 'Right Pial Mesh',
              'Left White Mesh', 'Right White Mesh',
              'Left Resampled Pial', 'Right Resampled Pial',
              'Left Resampled White', 'Right Resampled White',
              'Left Gyri Texture', 'Right Gyri Texture',
              'Left Sulci/Gyri', 'Right Sulci/Gyri',
              'Left Resampled Gyri', 'Right Resampled Gyri',
              'Left Resampled Sulci/Gyri', 'Right Resampled Sulci/Gyri',
              'Left Resampled Curvature', 'Right Resampled Curvature',
              'Left Resampled Avg. Curvature',
              'Right Resampled Avg. Curvature',
              'Left Resampled Pial Curvature',
              'Right Resampled Pial Curvature',
              'Left Resampled Thickness',
              'Right Resampled Thickness',
              'Left Resampled Inflated White',
              'Right Resampled Inflated White',
              'Both Hemi. White', 'Both Hemi. Pial',
              'Both Hemi. Inflated White',
              'Both Hemi. Resampled Gyri', 'Both Hemi. Resampled Sulci/Gyri']

    custom_filt = [eval(filt) for filt in self.data_filters]
    if len(custom_filt) == 1:
        custom_filt = custom_filt * len(dtypes)
    if len(custom_filt) < len(dtypes):
        custom_filt = custom_filt + [{}] * (len(dtypes) - len(custom_filt))

    filter1 = {'_format': ('NIFTI-1 image', 'gz compressed NIFTI-1 image')}
    filter2 = {}
    filter3_l = {'side': 'left'}
    filter3_r = {'side': 'right'}

    filters = [filter1, filter1, filter2, filter3_l, filter3_r,
               filter3_l, filter3_r, filter3_l, filter3_r,
               filter3_l, filter3_r, filter3_l, filter3_r,
               filter3_l, filter3_r, filter3_l, filter3_r,
               filter3_l, filter3_r, filter3_l, filter3_r,
               filter3_l, filter3_r, filter3_l, filter3_r,
               filter3_l, filter3_r, filter3_l, filter3_r,
               filter2, filter2, filter2, filter2, filter2]
    for filt, custfilt in zip(filters, custom_filt):
        filt.update(custfilt)
    filters = [repr(filt) for filt in filters]

    self.proc = getProcessInstance('database_qc_table')
    return context.runProcess(self.proc, database=self.database,
                              data_types=dtypes,
                              data_filters=filters,
                              keys=self.keys,
                              type_labels=tlabels,
                              output_file=self.output_file)


