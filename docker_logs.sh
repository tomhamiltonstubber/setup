#!/usr/bin/env bash

port=${1:-5001}
while true; do
    until $(curl -q -so /dev/null http://localhost:$port/logs -I && true); do
        printf .
        sleep 0.1
    done
    curl -q -s http://localhost:$port/logs
    for i in `seq 1 10`; do
        printf '\n'
    done
    sleep 2
done
