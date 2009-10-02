import os

def launchFreesurferCommand(context, database, *args, **kwargs):
    os.environ['SUBJECTS_DIR'] = database
    context.system(*args, **kwargs)
