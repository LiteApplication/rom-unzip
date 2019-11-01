#!/bin/bash
srcPath=$2
echo "Removing old folders..."
sudo rm -fr rom-extracted
echo "Extracting ROM files..." 
unzip $1 -d rom-extracted -qq
cd rom-extracted
echo "Extracting system to dat"
sudo brotli --decompress system.new.dat.br --out system.new.dat
echo "Extracting vendor to dat"
sudo brotli --decompress vendor.new.dat.br --out vendor.new.dat
echo "Extracting system.dat to system.img"
$(srcPath)/sdat2img.py system.transfer.list system.new.dat system.img
echo "Extracting vendor.dat to vendor.img"
$(srcPath)/sdat2img.py vendor.transfer.list vendor.new.dat vendor.img
echo "Mounting system.img..."
mkdir system.mount
sudo mount -t ext4 -o loop system.img system.mount
echo "Mounting vendor.img..."
mkdir vendor.mount
sudo mount -t ext4 -o loop vendor.img vendor.mount
echo "Cleaning files..."
rm system.new.dat
rm system.new.dat.br
rm system.transfer.list
rm vendor.new.dat
rm vendor.new.dat.br
rm vendor.transfer.list
echo "Saving permissions for system.img..."
python $(srcPath)/savePerm.py system.mount
