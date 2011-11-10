# -*- coding: utf-8 -*-
import os
from neuroConfig import mainPath

print 'PATH'
print mainPath

#runFreesurferCommandSh = os.path.join( mainPath, '..', 'scripts', 'runFreesurferCommand.sh' )
#path_freesurfer = "/volatile/svn/source/cortical_surface/freesurfer_plugin/trunk/brainvisa/scripts/runFreesurferCommand.sh"

path_basename = os.path.dirname(mainPath)
print 'Dirname'
print path_basename

#runFreesurferCommandSh = os.path.join('/', 'volatile', 'svn', 'source', 'cortical_surface', 'freesurfer_plugin', 'trunk', 'scripts', 'runFreesurferCommand.sh' )
#runFreesurferCommandSh = os.path.join('/', 'volatile', 'svn', 'compil', 'scripts', 'runFreesurferCommand.sh' )
runFreesurferCommandSh = os.path.join(path_basename, 'scripts', 'runFreesurferCommand.sh' )


#runFreesurferCommandSh = '/volatile/svn/source/cortical_surface/freesurfer_plugin/trunk/brainvisa/scripts/runFreesurferCommand.sh'
print "PATH FREESURFER"
print runFreesurferCommandSh


#runFreesurferCommandSh = os.path.join( mainPath, 'toolboxes', 'freesurfer', 'scripts', 'runFreesurferCommand.sh' )
if not os.path.exists( runFreesurferCommandSh ):
 print "path don't exist"
 runFreesurferCommandSh = None
 
def launchFreesurferCommand( context, database, *args, **kwargs ):
  if database:
    os.environ[ 'SUBJECTS_DIR' ] = database
  print "comamnd"
  print runFreesurferCommandSh
  if runFreesurferCommandSh:
    print 'run'
    print args
    print kwargs
    context.system( *( ( runFreesurferCommandSh, ) + args ), **kwargs )
  else:
    print 'else'
    print args
    print kwargs
    context.system( *args, **kwargs )
