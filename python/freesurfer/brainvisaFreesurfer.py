# -*- coding: utf-8 -*-

import os
import platform
from brainvisa.configuration.neuroConfig import sharePath
import brainvisa.processes
from soma.wip.application.api import Application
from brainvisa.validation import ValidationError
import shutil

configuration = Application().configuration


# print("Module brainvisafreesurfer.py")

__freeSurferOK__ = None


def testFreesurferCommand(force_retest=False):
    global __freeSurferOK__
    if force_retest or __freeSurferOK__ is None:
        context = brainvisa.processes.defaultContext()
        try:
            launchFreesurferCommand(context, None, 'mri_convert', '-h')
            __freeSurferOK__ = True
        except:
            __freeSurferOK__ = False
    if not __freeSurferOK__:
        raise ValidationError('FreeSurfer not available.')


def launchFreesurferCommand(context, database=None, *args, **kwargs):
    if platform.system() == 'Windows':
        raise ValidationError('FreeSurfer plugin for BrainVISA is not available '
                              'on Windows platform.')

    # print(" -- Function launchFreesurferCommand -- ", args)
    # print('kwargs:', kwargs)

    # INI PATH SCRIPT TO RUN FREESURFER
    path_basename = os.path.dirname(os.path.dirname(sharePath))
    runFreesurferCommandSh = os.path.join(
        path_basename, 'scripts', 'runFreesurferCommand.sh')
    if not os.path.exists(runFreesurferCommandSh):
        # print("path don't exist")
        runFreesurferCommandSh = None

    # INI FREESURFER DATABASE  : it seems no mandatory to set SUBJECTS_DIR to run some of freesurfer commands, but some of them
    # require this variable
    if not database:
        database = configuration.freesurfer.subjects_dir_path
    if database:
        os.environ['SUBJECTS_DIR'] = database
    # else hope the environment variable SUBJECTS_DIR is already set.

    # Try with the freesurfer shell script otherwise the exec
    # shell freesurfer script
    setupShell = []
    # It seems not necessary to test the SHELL variable to try to guess the bash
    # It seems not necessary to use executable_freesurfer
    # if configuration.freesurfer.freesurfer_home_path :
    #  if  os.getenv( 'SHELL' ) == "/bin/bash" :
    #    setupShell.append(configuration.freesurfer.freesurfer_home_path + "/FreeSurferEnv.sh")
    #  else : setupShell.append(configuration.freesurfer.freesurfer_home_path + "/FreeSurferEnv.csh")
    # elif configuration.freesurfer.executable_freesurfer :
    # setupShell.append(configuration.freesurfer.executable_freesurfer)

    if configuration.freesurfer.freesurfer_home_path \
            and os.path.exists(configuration.freesurfer.freesurfer_home_path):
        # force FREESURFER_HOME in case it is not defined or if it points to
        # another version
        os.environ['FREESURFER_HOME'] \
            = configuration.freesurfer.freesurfer_home_path

    # determine freesurfer commands path or environment script
    if configuration.freesurfer.freesurfer_home_path \
        and os.path.exists(os.path.join(
                           configuration.freesurfer.freesurfer_home_path, 'FreeSurferEnv.sh')):
        setupShell.append(os.path.join(
                          configuration.freesurfer.freesurfer_home_path, 'FreeSurferEnv.sh'))
    else:
        # test a freesurfer command
        cmdFreeSurferSystem = shutil.which(args[0])
        if cmdFreeSurferSystem:
            # run directly without setting environment
            try:
                context.system(* args, nativeEnv=True, **kwargs)
                return
            except Exception as e:
                context.warning('direct run failed:', e)
                ret = 2
        else:
            # hope FreeSurferEnv.sh is in the path, but few chances...
            cmdFreeSurferSystem = shutil.which(
                "FreeSurferEnv.sh")
            if cmdFreeSurferSystem:
                setupShell.append("FreeSurferEnv.sh")
            else:
                # FreeSurfer is really not found, here.
                raise ValidationError('FreeSurfer is not available')

    argShell = tuple(setupShell) + args

    try:
        ret = context.system(*((runFreesurferCommandSh, ) + argShell),
                             nativeEnv=True, **kwargs)
    except Exception as e:
        ret = 2
    if ret != 0:
        raise ValidationError(
            'FreeSurfer not available or one freesurfer command line has failed. Please see the log file in the main menu of BrainVISA for more information.\nException: %s' % str(e))
