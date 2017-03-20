#! /bin/sh
script=$(dirname "$0")'/strip_ipynb.py'
python $script "$@"
