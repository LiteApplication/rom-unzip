#!/usr/bin/python3
# coding: utf8

#Modules import
import argparse
import os
from termcolor import colored
from pwd import getpwuid
from grp import getgrgid
import json
import glob
import shutil
import sys
import zipfile
from datetime import datetime

#Argument parser
ap = argparse.ArgumentParser(description="Unzip an Android rom to system.img and vendor.img. ")
ap.add_argument("-v","--version",     action="store_true", help="Show the script version and exit. ")
ap.add_argument("-V","--verbose",     action="store_true", help="Verbosely run script. ")
ap.add_argument("-n","--no-update",   action="store_true", help="Block auto-update. ")
ap.add_argument("-l","--log",         action="store_true", help="Save output to rom-unzip.log. ")
ap.add_argument("-a","--all",         action="store_true", help="Run all steps, enabled by default. ")
ap.add_argument("-u","--update",      action="store_true", help="Update program and exit. ")
ap.add_argument("-r","--resume",      action="store_true", help="Resume previous rom extracting. ")
ap.add_argument("-s","--show-saved",  action="store_true", help="Show the actual saved state and exit. ",                   dest='saved')
ap.add_argument("-p","--rom-path",    action="store",      help="The path to rom.zip folder. ",                             dest='path',    default=".")
ap.add_argument("-m","--step",        action="store",      help="Run only one step of rom-unzip. Pass 0 to view options. ", dest='step',    default="-1",  type=int, )
ap.add_argument("-o","--option",      action="store",      help="Argument for single step.",                                dest='opt',     default="")
ap.add_argument("-e","--extract-dir", action="store",      help="Path to extract rom. ",                                    dest='extract', default="rom-extracted")


args = ap.parse_args()
if args.step == -1:
    args.all = True
else:
    args.all = False

class rom_toolbox:
    __doc__ = """This class is a toolbox for rom_unzip\n"""
    def select(self, runDir="NoDir"): #return a rom zip (absolute path) from runDir
        show("Start rom_toolbox.select()")
        if runDir=="NoDir":
            runDir=os.getcwd()
            show("No command, selecting cwd")
        ROM_FILES=['system.new.dat.br','vendor.new.dat.br','system.transfer.list','vendor.transfer.list']
        show("Finding ROM zip file...")
        availableZip=glob.glob(runDir+"/*.zip")
        availableRom=[]
        for zipp in availableZip:
            zipf = zipfile.ZipFile(zipp)
            add=False
            for file in ROM_FILES:
                if file in zipf.namelist():
                    add=True
            if add:
               availableRom.append(zipp)
        if len(availableRom)>= 2:
            print("Multiple ROMs are available in this directory : ")
            rom=self.chooseFile(availableRom)
        elif availableRom==[]:
            return "NOROM"
        else:
            rom=availableRom[0]
        return rom
    def unzip(self, source,path):
        show("Extracting rom files...")
        zipfile.ZipFile(source, 'r').extractall(path)
    def unbr(self, source,path):
        os.system("brotli -d " + source + " -o " + path + "> /dev/null")
    def chooseFile(self, files):
        for i,file in zip(range(1,len(files)),files):
            print("\t"+str(i)+" : "+os.path.splitext(os.path.basename(file))[0])
        print("\n\t0 : Exit")
        try:
            choice = int(input("Your choice : "))-1
        except ValueError:
            print("Wrong entry type, press 0 to exit")
            self.chooseFile(files)
        if choice == -1:
            print("Exiting...")
            exit(0)
        else:
            return files[choice]
    def listFiles(self, rootdir):
        for (cur,subdir,files) in os.walk('Test', topdown=True): 
            for element in subdir+files:
                yield cur + "/" + element

class rom_unzip:
    __doc__ = """This class allow you to extract Android Roms into system and vendor folders."""
    __version__ = open("/etc/liteapplication/rom-unzip/version").readline()
    rom=""
    def run_all(self):
        self.import_modules()
        self.rom = self.select_rom(args.path)
        self.create_dir(args.extract)
        self.set_state(3, ".")
        self.unzip_rom(self.rom)
        self.set_state(4, ".")
        self.unzip_brotli()
        self.set_state(5, ".")
        self.extract_dat()
        self.set_state(6, ".")
        self.save_img()
        self.set_state(7, ".")
    def resume(self):
        os.chdir(args.extract)
        i = int(self.get_state("."))
        #if i<4:
        #    self.run_all()
        for s in range(i+1, 8):
            self.run_step(s)
    def show_steps(self):
        print("0 : show_steps")
        print("1 : import_modules")
        print("2 : select_rom")
        print("3 : create_dir")
        print("4 : unzip_rom")
        print("5 : unzip_brotli")
        print("6 : extract_dat")
        print("7 : save_img")
    def run_step(self,n):
        steps = {
            0 : self.show_steps,
            1 : self.import_modules,
            2 : self.select_rom,
            3 : self.create_dir,
            4 : self.unzip_rom,
            5 : self.unzip_brotli,
            6 : self.extract_dat,
            7 : self.save_img,
        }
        if args.opt == "":
            steps[n]()
        else:
            steps[n](args.opt)
    def import_modules(self):
        try:
            show("Importing python files...")
        except ImportError:
            print("E05: ImportError")
            exit(1)
    def select_rom(self, romdir):
        rompath=tb.select(path(romdir))
        if rompath=="NOROM":
            print(colored("E02 : NoRomError, Please cd to the rom.zip folder","red"))
            exit(1)
        if not os.path.isfile(rompath):
            print(colored("E03 : NotFileError, The selected ROM is not a file (" + rompath + ").Please cd to the rom.zip folder and select it. ","red"))
            exit(1)
        return rompath
    def create_dir(self, extract):
        try:
            os.mkdir(extract,0o777)
        except FileExistsError:
            shutil.rmtree(extract)
            os.mkdir(extract,0o777)
            pass
        os.chdir(path(extract))
    def unzip_rom(self, rompath):
        tb.unzip(path(rompath),path("."))
    def unzip_brotli(self):
        show("Extracting system.new.dat.br...")
        tb.unbr(path("system.new.dat.br"),"system.new.dat")
        show("Extracting vendor.new.dat.br...")
        tb.unbr(path("vendor.new.dat.br"),"vendor.new.dat")
    def extract_dat(self):
        show("Extracting system.img ...")
        o=""
        if args.log:
            o = " -d ./rom-unzip-logs.txt"
        os.system("sudo python2 /etc/liteapplication/rom-unzip/sdat2img.py " + path("system.transfer.list") + " " + path("system.new.dat") + " system.img" + o)
        show("Extracting vendor.img ...")
        os.system("sudo python2 /etc/liteapplication/rom-unzip/sdat2img.py " + path("vendor.transfer.list") + " " + path("vendor.new.dat") + " vendor.img" + o)
    def save_img(self):
        show("Mounting system.img ...")
        os.system("mkdir system.dir")
        os.system("sudo mount -t ext4 -o loop system.img system.dir/")
        show("Mounting vendor.img ...")
        os.system("mkdir vendor.dir")
        os.system("sudo mount -t ext4 -o loop vendor.img vendor.dir/")
        os.system("sudo nautilus " + args.extract+" > /dev/null")
        unnecessary_files = ["system.new.dat.br","system.new.dat","system.transfer.list","vendor.new.dat.br","vendor.new.dat","vendor.transfer.list"]
        for file in unnecessary_files:
            try:
                os.remove(file)
                show("Removed '{}'".format(file))
            except:
                show("Unable to remove '{}'".format(file))
    def set_state(self, state, dest):
        if not os.path.exists(dest+"/.state.save"):
            os.mknod(dest+"/.state.save")
        with open(dest+"/.state.save","w") as f:
            content = f.readlines()
            content[0] = str(state)
            content[1] = self.rom
            f.write(content)
    def get_state(self, dest):
        with open(dest+"/.state.save","r+") as f:
            return str(f.readlines()[0])

def show(message):
    now = datetime.now()
    message = "[ " + now.strftime("%d/%m %H:%M:%S") + " ] MEM : "+ mem() + " MB :\t" + message
    if args.verbose:
        print(message)
    if args.log:
        with open("./rom-unzip-logs.txt","a") as f:
            f.write(message+" \r\n")
def mem():
    import subprocess
    out = subprocess.Popen(['ps', 'v', '-p', str(os.getpid())],
    stdout=subprocess.PIPE).communicate()[0].split(b'\n')
    vsz_index = out[0].split().index(b'RSS')
    mem = float(out[1].split()[vsz_index]) / 1024
    return str(mem)
def path(s):
    return os.path.abspath(glob.glob(s)[0])
if os.geteuid() != 0:
    print("Please run this script as root\nwith 'sudo "+sys.argv[0]+"'")
    print("CODE : 1")
    exit(1)
last = float(os.system("curl -s https://raw.githubusercontent.com/LiteApplication/rom-unzip/master/src/version"))
if float(rom_unzip.__version__) < float(last) and not args.no_update:
    show("Updating ...")
    os.system("curl -s https://raw.githubusercontent.com/LiteApplication/rom-unzip/master/install | sudo bash > /dev/null")
try:
    show("Rom-unzip by LiteApplication v" + str(rom_unzip.__version__))
    show("Step      : " + str(args.step))
    show("Log       : " + str(args.log))
    show("Verbose   : " + str(args.verbose))
    show("All       : " + str(args.all))
    show("Version   : " + str(args.version))
    show("Resume    : " + str(args.resume))
    show("Update    : " + str(args.update))
    show("Saved     : " + str(args.saved))
    show("Option    : " + str(args.opt))
    show("Rom path  : " + str(args.path))
    show("Extract   : " + str(args.extract))
    ru = rom_unzip()
    tb = rom_toolbox()
    if args.version:
        print("Rom-unzip by LiteApplication v" + str(rom_unzip.__version__))
        exit(0)
    elif args.update:
        show("Updating ...")
        os.system("curl -s https://raw.githubusercontent.com/LiteApplication/rom-unzip/master/install | sudo bash")
        exit(0)
    if args.resume:
        ru.resume()
    elif int(args.step) > -1 and int(args.step) <= 8:
        ru.run_step(args.step)
    elif int(args.step) <= -1 and int(args.step) > 9:
        ru.run_all()
    elif args.saved:
        print(ru.get_state(args.extract))
    elif args.all:
        ru.run_all()
except KeyboardInterrupt:
    show("Exiting...")
    exit(0)