#!/bin/bash

time ./hydrometer.py -s > ~/Desktop/sf_raw.txt

time ./hydrometer.py -g > ~/Desktop/github_raw.txt

time ./hydrometer.py -n > ~/Desktop/gnu_raw.txt

time ./hydrometer.py -c > ~/Desktop/googlecode_raw.txt

