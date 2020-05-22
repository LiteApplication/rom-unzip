# ROM Unzip
Unzip an Android ROM to system and vendor
## One-line: 
`curl -s https://raw.githubusercontent.com/LiteApplication/rom-unzip/master/install | sudo bash && rom-unzip -Vla`
## Usage
The easiest way to extract rom is to run `sudo rom-unzip` in the rom folder and to wait about 10 minutes without using computer until you see your shell prompt.\
If you want to see the progression, run `sudo rom-unzip -V`. To resume an old extract, go to the same folder, run the same command and add `-r` at the bottom (BETA)
```
usage: rom-unzip [-h] [-v] [-V] [-l] [-a] [-u] [-r] [-s] [-p PATH] [-m STEP]
                 [-o OPT] [-e EXTRACT]

Unzip an Android rom to system.img and vendor.img.

optional arguments:
  -h, --help                 Show this help message and exit
  -v, --version              Show the script version and exit.
  -V, --verbose              Verbosely run script.
  -l, --log                  Save output to rom-unzip.log.
  -a, --all                  Run all steps, enabled by default.
  -u, --update               Update program and exit.
  -r, --resume               Resume previous rom extracting.
  -s, --show-saved           Show the actual saved state and exit.
  -p, --rom-path PATH        The path to rom.zip folder.
  -m, --step STEP            Run only one step of rom-unzip. Pass 0 to view options.
  -o, --option OPT           Argument for single step.
  -e, --extract-dir EXTRACT  Path to extract rom.
```
## Installation
Just run `curl -s https://raw.githubusercontent.com/LiteApplication/rom-unzip/master/install | sudo bash` to install ROM-Unzip.\
If you want to download the file for run it later, install on multiple computer or read it from your computer, you can download it at [raw.github.com](https://raw.githubusercontent.com/LiteApplication/rom-unzip/master/install)\
To install the program , just run `./install` , no need to download the entire repository, just download and run install.  
## Performances
Extract an Android 10 ROM with Gapps (1,13GB) take 13 seconds with 8GB RAM, 8 cores. The result is 3,2GB. 
## Credits
- [sdat2img](https://github.com/xpirt/sdat2img) by @xpirt
