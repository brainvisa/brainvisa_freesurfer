# -*- coding: utf-8 -*-
import os
from neuroConfig import mainPath

path_basename = os.path.dirname(mainPath)

runFreesurferCommandSh = os.path.join(path_basename, 'scripts', 'runFreesurferCommand.sh' )

#runFreesurferCommandSh = os.path.join( mainPath, 'toolboxes', 'freesurfer', 'scripts', 'runFreesurferCommand.sh' )
if not os.path.exists( runFreesurferCommandSh ):
 #print "path don't exist"
 runFreesurferCommandSh = None
 
def launchFreesurferCommand( context, database, *args, **kwargs ):
  if database:
    os.environ[ 'SUBJECTS_DIR' ] = database
  #print "comamnd"
  #print runFreesurferCommandSh
  if runFreesurferCommandSh:
    #print 'run'
    #print args
    #print kwargs
    context.system( *( ( runFreesurferCommandSh, ) + args ), **kwargs )
  else:
    #print 'else'
    #print args
    #print kwargs
    context.system( *args, **kwargs )
