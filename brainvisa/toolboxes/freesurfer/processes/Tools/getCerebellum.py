from brainvisa.processes import *

name = 'Get Cerebellum in split mask'

signature = Signature(
  'FS_aseg', ReadDiskItem( 'T1 MRI', 'aims readable volume formats' ),
  'split_mask', ReadDiskItem( 'Split brain mask', 'aims readable volume formats' ),
  'output_split_mask', WriteDiskItem( 'Split brain mask', 'aims writable volume formats' ),
)

def initialization( self ):
  self.linkParameters( 'split_mask', 'FS_aseg' )
  self.linkParameters( 'output_split_mask', 'split_mask' )
  
def execution( self, context ):
  context.system( sys.executable, '-m', 'freesurfer.get_cerebellum', self.FS_aseg, self.split_mask, self.output_split_mask )

