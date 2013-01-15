# -*- coding: utf-8 -*-
import os
from brainvisa.configuration.neuroConfig import mainPath
import brainvisa.processes
from soma.wip.application.api import Application
from brainvisa.validation import ValidationError
import distutils.spawn

configuration = Application().configuration


#print "Module brainvisafreesurfer.py"

__freeSurferOK__ = None

def testFreesurferCommand( force_retest=False ):
  global __freeSurferOK__
  if force_retest or __freeSurferOK__ is None:
    context = brainvisa.processes.defaultContext()
    try:
      launchFreesurferCommand(context, None, 'mri_convert', '-h')
      __freeSurferOK__ = True
    except:
      __freeSurferOK__ = False
  if not __freeSurferOK__:
    raise ValidationError( 'FreeSurfer not available.' )


def launchFreesurferCommand( context, database=None, *args, **kwargs ):
  #print " -- Function launchFreesurferCommand -- ", args
  #print 'kwargs:', kwargs
  
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
  else :  database = configuration.freesurfer.subjects_dir_path
 

  #Try with the freesurfer shell script otherwise the exec
  #shell freesurfer script
  setupShell = []
  #It seems not necessary to test the SHELL variable to try to guess the bash
  ##It seems not necessary to use executable_freesurfer
  #if configuration.freesurfer.freesurfer_home_path :
  #  if  os.getenv( 'SHELL' ) == "/bin/bash" :
  #    setupShell.append(configuration.freesurfer.freesurfer_home_path + "/FreeSurferEnv.sh")
  #  else : setupShell.append(configuration.freesurfer.freesurfer_home_path + "/FreeSurferEnv.csh")
  #elif configuration.freesurfer.executable_freesurfer : setupShell.append(configuration.freesurfer.executable_freesurfer)
  

  #At first test a freesurfer command 
  cmdFreeSurferSystem = distutils.spawn.find_executable("mri_convert")
  if distutils.spawn.find_executable("mri_convert") :
    context.system ( * args,  **kwargs )
  else:
    if configuration.freesurfer.freesurfer_home_path:
      setupShell.append( os.path.join( configuration.freesurfer.freesurfer_home_path + "/FreeSurferEnv.sh" ) )
    else:
      # hope FreeSurferEnv.sh is in the path, but few chances...
      setupShell.append( "FreeSurferEnv.sh" )
    argShell = tuple(setupShell) + args

    try :
      ret = context.system ( *( (runFreesurferCommandSh, ) + argShell ),  **kwargs )
    except Exception, e:
      ret = 2
    if ret != 0:
      raise ValidationError( 'FreeSurfer not available or one freesurfer command line has failed. Please see the log file in the main menu of BrainVISA for more information.' )

