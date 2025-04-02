#!/bin/bash

export FLAG=${FLAG:-"flag{example_flag}"}

while true; do
    socat TCP-LISTEN:9000,reuseaddr,fork,keepalive EXEC:/app/main
done
