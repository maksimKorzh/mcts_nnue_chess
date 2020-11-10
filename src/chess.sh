#!/bin/bash

BASEDIR=$(dirname "$0")
cd $BASEDIR
exec python3 engine.py
