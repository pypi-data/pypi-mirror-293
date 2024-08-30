#!/bin/sh

BASE_DIR=$(dirname "$0")
cd "$BASE_DIR"
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
