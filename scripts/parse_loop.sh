#!/bin/bash

EXITCODE=0

while [ "$EXITCODE" -eq 0 ]; do
    sbt "runMain pisa.server.PisaOneStageServer8000" & PID1=$! 
    sleep 20
    python3 src/main/python/initial_parse.py --all_files /pisa/all_files.json --current /pisa/current.json & PID0=$! 
    echo "PID0 (python client): $PID0"
    echo "PID1: (server)$PID1"
    wait $PID0
    EXITCODE=$?
    echo "EXITCODE: $EXITCODE"

    # if [ "${exit_status}" - 0 ];
    # then
    #     echo "exit ${exit_status}"
    # fi
    # echo "EXIT 0"

    PID0_CHILDREN=`pstree -l -p $PID0 |grep "([[:digit:]]*)" -o |tr -d '()'`
    if [ -z "$PID0_CHILDREN" ]; then
        echo "PID0_CHILDREN is empty"
    else
        echo "Echo 0 killing: $PID0_CHILDREN"
        kill $PID0_CHILDREN
    fi

    PID1_CHILDREN=`pstree -l -p $PID1 |grep "([[:digit:]]*)" -o |tr -d '()'`
    if [ -z "$PID1_CHILDREN" ]; then
        echo "PID1_CHILDREN is empty"
    else
        echo "Killing server children"
        kill $PID1_CHILDREN
    fi

    # echo "Echo 1 killing: "
    # echo `pstree -l -p $PID1 |grep "([[:digit:]]*)" -o |tr -d '()'`
    # kill `pstree -l -p $PID1 |grep "([[:digit:]]*)" -o |tr -d '()'`

    # ps aux |grep scala | awk '{print $2}' | xargs kill
    # ps aux |grep java | awk '{print $2}' | xargs kill
    # ps aux |grep poly | awk '{print $2}' | xargs kill

done