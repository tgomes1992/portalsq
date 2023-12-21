#!/bin/bash

aplicacao=`ps aux | grep -m1 portal-escrituracao | awk {'print $11'}`

if [ "$aplicacao" == "bash" ] || [ "$aplicacao" == "python" ];
  then
    echo "Aplicacao Up, Matando!" > /tmp/kill.log
    for pid in $(ps aux | grep -m1 portal-escrituracao | awk {'print $2'} )
       do 
         kill -9 $pid
       done
  else
    echo "Aplicacao Down" > /tmp/kill.log
fi