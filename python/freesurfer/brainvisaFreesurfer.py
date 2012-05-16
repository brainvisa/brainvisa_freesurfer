# -*- coding: utf-8 -*-
import os
from brainvisa.configuration.neuroConfig import mainPath
import brainvisa.processes
from soma.wip.application.api import Application
from brainvisa.validation import ValidationError
import distutils.spawn

configuration = Application().configuration


#print "Module brainvisafreesurfer.py"


def testFreesurferCommand( *args, **kwargs ):
  #print " -- Function testFreesurferCommand -- "
  context = brainvisa.processes.defaultContext()
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
    setupShell.append(configuration.freesurfer.freesurfer_home_path + "/FreeSurferEnv.sh")
    argShell = tuple(setupShell) + args
    #print args
    #print kwargs
  
    #freesurfer exec
    #print "Test avec exec"
    #setupExec = []
    #setupExec.append(configuration.freesurfer.executable_freesurfer)
    #print setupExec
    #argExec = tuple(setupExec) + args
    #print argExec
  
    #print "ArgShell"
    #print argShell
  
    #try :  
      #context.system ( *( (runFreesurferCommandSh, ) + argShell ),  **kwargs )
    #except:
      #try: 
        #context.system ( *( (runFreesurferCommandSh, ) + argExec ),  **kwargs )
      #except:  
        #raise ValidationError( 'FreeSurfer not available' )

    try :  
      context.system ( *( (runFreesurferCommandSh, ) + argShell ),  **kwargs )
    except:  
      raise ValidationError( 'FreeSurfer not available' )
  
