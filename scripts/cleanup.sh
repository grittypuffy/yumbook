#!/bin/sh
DIR="../"
find $DIR -type f -wholename "*.synctex.gz" -print0 -exec rm -rf {} \;
find $DIR -type f -name "*.log" -print0 -exec rm -rf {} \;
find $DIR -type d -name "auto/" -print0 -exec rm -rf {} \;
