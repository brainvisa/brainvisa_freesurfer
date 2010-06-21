#!/bin/sh

if [ -n "$FREESURFER_HOME" ]; then
  source "${FREESURFER_HOME}/FreeSurferEnv.sh"
fi
exec "$@"
