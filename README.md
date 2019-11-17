# ROM Unzipper
Unzip an Android ROM to system and vendor
## Installation
Just run `curl -s https://raw.githubusercontent.com/LiteApplication/rom-unzip/master/install | sudo bash` to install ROM-Unzip.\
If you want to download the file for run it later, install on multiple computer or read it from your computer, you can download it at [raw.github.com](https://raw.githubusercontent.com/LiteApplication/rom-unzip/master/install)
## Usage
To install the program , just run ./install , no need to download the entire repository, just download and run install.\
To extract a rom, cd to the rim folder and run rom-unzip.
The extracting can take a long time, try to be patient
## Developpement progress
- [x] Find the ROMs
- [x] Check if ROMs is valid
- [x] Select if needed
- [x] Unzip the ROM
- [x] Extract system.new.dat.br
- [x] Extract vendor.new.dat.br
- [x] Convert system.new.dat into system.img
- [x] Convert vendor.new.dat into vendor.img
- [x] Mount system.img
- [x] Save permissions for system.img
- [ ] Mount vendor.img
- [ ] Save permissions for vendor.img
- [ ] Copy system files to a folder
- [ ] Copy vendor files to a folder
- [ ] Removing permissions to allow RW on vendor and system

## Credits
- [sdat2img](https://github.com/xpirt/sdat2img) by xpirt
