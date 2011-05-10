# -*- coding: utf-8 -*-
import os
from neuroConfig import mainPath

runFreesurferCommandSh = os.path.join( mainPath, 'toolboxes', 'freesurfer', 'scripts', 'runFreesurferCommand.sh' )
if not os.path.exists( runFreesurferCommandSh ):
 runFreesurferCommandSh = None
 
def launchFreesurferCommand( context, database, *args, **kwargs ):
  if database:
    os.environ[ 'SUBJECTS_DIR' ] = database
  if runFreesurferCommandSh:
    print 'run'
    print args
    print kwargs
    context.system( *( ( runFreesurferCommandSh, ) + args ), **kwargs )
  else:
    context.system( *args, **kwargs )
