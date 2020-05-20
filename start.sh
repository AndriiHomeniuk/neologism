#!/bin/bash
app="neologism"
docker build -t ${app} .
docker run -d -p 5005:80 --name=${app} -v $PWD:/app ${app}