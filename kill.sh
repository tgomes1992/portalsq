#!/bin/bash

aplicacao=`ps aux | grep -m1 portal-escrituracao | awk {'print $11'}`

if [ "$aplicacao" == "python" ]; then
    pid=`ps aux | grep -m1 portal-escrituracao | awk {'print $2'}`
    kill -9 $pid
    exit
fi
