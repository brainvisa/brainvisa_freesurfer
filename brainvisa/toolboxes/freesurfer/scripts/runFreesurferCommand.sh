#!/bin/bash

if [ -n "$FREESURFER_HOME" ]; then
 # source "${FREESURFER_HOME}/SetUpFreeSurfer.sh"
  source "${FREESURFER_HOME}/FreeSurferEnv.sh"
fi
exec "$@"
