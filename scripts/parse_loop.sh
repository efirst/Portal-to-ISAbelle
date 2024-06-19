#!/bin/bash

# DATASET="afp"
# DATASET_DIR="/pisa/afp/thys"
# OUTPUT_DIR="/pisa/output"

DATASET="hol"
DATASET_DIR="/pisa/Isabelle2022/src/HOL"
OUTPUT_DIR="/pisa/output"

DATASET="hol-imp"
DATASET_DIR="/pisa/Isabelle2022/src/HOL"
OUTPUT_DIR="/pisa/output"

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

python3 src/main/python/preprocess_dataset.py --name $DATASET --dataset-dir $DATASET_DIR

while [ "$EXITCODE" -eq 0 ]; do
    sbt "runMain pisa.server.PisaOneStageServer8000" & server_pid=$! 
    sleep 20
    python3 src/main/python/initial_parse.py --output-dir $OUTPUT_DIR/$DATASET & client_pid=$! 
    echo "client_pid (python client): $client_pid"
    echo "server_pid: $server_pid"
    wait $client_pid
    EXITCODE=$?
    echo "EXITCODE: $EXITCODE"

    clean_up_child_processes $client_pid
    clean_up_child_processes $server_pid
done