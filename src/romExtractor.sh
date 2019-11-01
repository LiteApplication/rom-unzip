#!/bin/bash
echo "Removing old folders..."
rm -fr rom-extracted
echo "Extracting ROM files..." 
unzip $1 -d rom-extracted -qq
cd rom-extracted



