#!/bin/bash


echo $0
echo $1
echo $@

#if [ -n "$FREESURFER_HOME" ]; then
  #echo "dans if"
  #source "$1"
 ## source "${FREESURFER_HOME}/SetUpFreeSurfer.sh"
  #source "${FREESURFER_HOME}/FreeSurferEnv.sh"
#fi

#source "$1"
. "$1"
shift
echo $@
exec "$@"
