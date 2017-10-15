
from brainvisa.processes import *

name = 'Freesurfer / BrainVISA QC table'
userLevel = 0

signature = Signature(
    'database', Choice(),
    'keys', ListOf(String()),
    'data_filters', ListOf(String()),
)


def initialization(self):
    # list of possible databases, while respecting the ontology
    # ontology: brainvisa-3.2.0
    databases = [h.name for h in neuroHierarchy.hierarchies()
                 if h.fso.name == "freesurfer"]
    self.signature["database"].setChoices(*databases)
    if len(databases) >= 1:
        self.database = databases[0]
    else:
        self.signature["database"] = OpenChoice()

    self.setOptional('data_filters')
    self.keys = ['subject']


def execution(self, context):
    dtypes = ['RawFreesurferAnat', 'Ribbon Freesurfer',
              'Freesurfer Scanner To MNI Transformation',
              'Pial', 'Pial', 'White', 'White']

    filter1 = {'_format': ('NIFTI-1 image', 'gz compressed NIFTI-1 image')}
    filter2 = {}
    filter3_l = {'side': 'left'}
    filter3_r = {'side': 'right'}

    filters = [filter1, filter1, filter2, filter3_l, filter3_r,
               filter3_l, filter3_r, ]
    filters = [repr(filt) for filt in filters]

    context.write('filters:', filters)
    self.proc = getProcessInstance('database_qc_table')
    return context.runProcess(self.proc, database=self.database,
                              data_types=dtypes,
                              data_filters=filters,
                              keys=self.keys)

