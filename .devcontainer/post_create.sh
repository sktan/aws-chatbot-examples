#!/bin/bash

npm install -g aws-cdk
(
    cd hello-world || return
    pip install -r <(pipenv requirements --dev)
)
