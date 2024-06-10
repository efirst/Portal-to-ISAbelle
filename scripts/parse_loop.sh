#!/bin/bash

EXITCODE=0

while [ "$EXITCODE" -eq 0 ]; do

    python3 src/main/python/initial_parse.py --all_files /pisa/all_files.json --current /pisa/current.json --resume & PID0=$!
    wait $PID0
    EXITCODE=$?
    echo $EXITCODE

    # if [ "${exit_status}" - 0 ];
    # then
    #     echo "exit ${exit_status}"
    # fi
    # echo "EXIT 0"

    kill `pstree -l -p $PID0 |grep "([[:digit:]]*)" -o |tr -d '()'`

    ps aux |grep scala | awk '{print $2}' | xargs kill
    ps aux |grep java | awk '{print $2}' | xargs kill
    ps aux |grep poly | awk '{print $2}' | xargs kill

done