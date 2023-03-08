#!/bin/bash

/usr/bin/find . -name *.drawio -exec rm -f {}.pdf \; -exec drawio --crop -x -o {}.pdf {} \;
