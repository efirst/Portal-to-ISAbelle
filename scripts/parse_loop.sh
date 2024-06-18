#!/bin/bash

EXITCODE=0

clean_up_child_processes () {
    local pid=$1 # expects pid as argument
    local children=`pstree -l -p $pid |grep "([[:digit:]]*)" -o |tr -d '()'`
    if [ -z "$children" ]; then
        echo "$pid has no children"
    else
        echo "cleaning $pid and ${#children[@]} children"
        kill $children
    fi
}

while [ "$EXITCODE" -eq 0 ]; do
    sbt "runMain pisa.server.PisaOneStageServer8000" & server_pid=$! 
    sleep 20
    python3 src/main/python/initial_parse.py --all_files /pisa/all_files.json --current /pisa/current.json & client_pid=$! 
    echo "client_pid (python client): $client_pid"
    echo "server_pid: $server_pid"
    wait $client_pid
    EXITCODE=$?
    echo "EXITCODE: $EXITCODE"

    clean_up_child_processes $client_pid
    clean_up_child_processes $server_pid
done