#!/bin/bash

DIR=`echo $(cd "$(dirname "$0")"; pwd)`
LOGDIR="${DIR}/../logs"

sourcelogpath="${LOGDIR}/uwsgi.log"
touchfile="${LOGDIR}/touchforlogrotat"


DATE=`date -d "yesterday" +"%Y%m%d"`
destlogpath="${LOGDIR}/uwsgi.log.${DATE}"

mv $sourcelogpath $destlogpath
touch $touchfile
