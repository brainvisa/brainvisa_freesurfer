# -*- coding: utf-8 -*-
import os
from neuroConfig import mainPath
import neuroProcesses
from soma.wip.application.api import Application
from brainvisa.validation import ValidationError


configuration = Application().configuration


#print "Module brainvisafreesurfer.py"


def testFreesurferCommand( *args, **kwargs ):
  #print " -- Function testFreesurferCommand -- "
  context = neuroProcesses.defaultContext()
  launchFreesurferCommand(context, None, 'mri_convert', '-h')


def launchFreesurferCommand( context, database=None, *args, **kwargs ):
  #print " -- Function launchFreesurferCommand -- "
  
  #INI PATH SCRIPT TO RUN FREESURFER
  path_basename = os.path.dirname(mainPath)
  runFreesurferCommandSh = os.path.join(path_basename, 'scripts', 'runFreesurferCommand.sh' )
  #runFreesurferCommandSh = '/volatile/svn/source/cortical_surface/freesurfer_plugin/trunk/brainvisa/scripts/runFreesurferCommand.sh'
  if not os.path.exists( runFreesurferCommandSh ):
    #print "path don't exist"
    runFreesurferCommandSh = None
 
 
  #INI FREESURFER DATABASE  : it seems no mandatory to set SUBJECTS_DIR to run some of freesurfer commands, but some of them
  #require this variable
  if database:
    os.environ[ 'SUBJECTS_DIR' ] = database


  #Try with the freesurfer shell script otherwise the exec
  #shell freesurfer script
  setupShell = []
  if configuration.freesurfer.freesurfer_home_path :
    if  os.getenv( 'SHELL' ) == "/bin/bash" :
      setupShell.append(configuration.freesurfer.freesurfer_home_path + "/FreeSurferEnv.sh")
    else : setupShell.append(configuration.freesurfer.freesurfer_home_path + "/FreeSurferEnv.csh")
  elif configuration.freesurfer.executable_freesurfer : setupShell.append(configuration.freesurfer.executable_freesurfer)
  
  argShell = tuple(setupShell) + args
  #print args
  #print kwargs
  
  #freesurfer exec
  #print "Test avec exec"
  setupExec = []
  setupExec.append(configuration.freesurfer.executable_freesurfer)
  #print setupExec
  argExec = tuple(setupExec) + args
  #print argExec
  
 
  try :  
    context.system ( *( (runFreesurferCommandSh, ) + argShell ),  **kwargs )
  except:
    raise ValidationError( 'FreeSurfer not available' )
  #else:
  #  context.system ( *( (runFreesurferCommandSh, ) + argExec ),  **kwargs )
  #finally:
  #  final-block
    
  
