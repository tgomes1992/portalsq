#!/bin/bash

aplicacao=`ps aux | grep -m1 portal-escrituracao | awk {'print $11'}`

if [ "$aplicacao" != "python" ];
  then
    echo "Iniciando Aplicação"
    source /data/projects/portal-escrituracao/bin/activate
    python /data/projects/portal-escrituracao/latest/src/app.py &
    deactivate
    exit
  else
    echo "Aplicação em Execução"
    exit
fi