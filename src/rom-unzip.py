#!/usr/bin/python3
# coding: utf8

#Modules import
import memory_profiler
import time
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
import urllib.request

#Save original performances
start_memory = memory_profiler.memory_usage()
start_time = time.time()

#Argument parser
ap = argparse.ArgumentParser(description="Unzip an Android rom to system.img and vendor.img. ")
ap.add_argument("-v","--version",     action="store_true", help="Show the script version and exit. ")
ap.add_argument("-V","--verbose",     action="store_true", help="Verbosely run script. ")
ap.add_argument("-n","--no-update",   action="store_true", help="Block auto-update. ")
ap.add_argument("-l","--log",         action="store",      dest="log",default="none",help="Run the script and save logs. ")
ap.add_argument("-a","--all",         action="store_true", help="Run all steps, enabled by default. ")
ap.add_argument("-u","--update",      action="store_true", help="Update program and exit. ")
ap.add_argument("-r","--resume",      action="store_true", help="Resume previous rom extracting. ")
ap.add_argument("-s","--show-saved",  action="store_true", help="Show the actual saved state and exit. ",                   dest='saved')
ap.add_argument("-U","--umount",  action="store_true", help="Unmount a previous extraction, needed before remove. The orther alternative is rebooting computer.",                   dest='umount')
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
        show("AvailableZipFiles : " + str(availableZip))
        availableRom=[]
        for zipp in availableZip:
            zipf = zipfile.ZipFile(zipp)
            add=False
            for file in ROM_FILES:
                if file in zipf.namelist():
                    show("ZipFile({}) : File '{}' available".format(zipp,file))
                    add=True
            if add:
               availableRom.append(zipp)
        if len(availableRom)>= 2:
            show("Multiple rom available : " + availableRom)
            print("Multiple ROMs are available in this directory : ")
            rom=self.chooseFile(availableRom)
        elif availableRom==[]:
            show("No rom available")
            return "NOROM"
        else:
            show("One rom available : " + availableRom[0])
            rom=availableRom[0]
        show("Returning rom "+ rom)
        return rom
    def unzip(self, source,path):
        show("Extracting rom files...")
        show("Started rom_toolbox.unzip()")
        zipfile.ZipFile(source, 'r').extractall(path)
    def unbr(self, source,path):
        show("Started rom_toolbox.unbr()")
        os.system("brotli -d " + source + " -o " + path + "> /dev/null")
    def chooseFile(self, files):
        for i,file in zip(range(1,len(files)),files):
            print("\t"+str(i)+" : "+os.path.splitext(os.path.basename(file))[0])
        print("\n\t0 : Exit")
        try:
            choice = int(input("Your choice : "))-1
        except ValueError:
            print("Wrong entry type, press 0 to exit")
            show("ValueError")
            self.chooseFile(files)
        if choice == -1:
            print("Exiting...")
            show("Exit(0)")
            exit(0)
        else:
            return files[choice]

class rom_unzip:
    __doc__ = """This class allow you to extract Android Roms into system and vendor folders."""
    __version__ = open("/etc/liteapplication/rom-unzip/version").readline()
    rom=""
    def run_all(self):
        show("Started run_all()")
        self.import_modules()
        self.rom = self.select_rom(args.path)
        show("Using " + self.rom)
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
        show("Extraction complete. ")
    def resume(self):
        show("Resuming ... ")
        os.chdir(args.extract)
        i = int(self.get_state("."))
        if i<4:
            self.run_all()
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
        show("Started ron_step(n)")
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
        if args.log or args.verbose:
            o = " -d ./rom-unzip-sdat2img.txt "
        os.system("sudo python2 /etc/liteapplication/rom-unzip/sdat2img.py " + path("system.transfer.list") + " " + path("system.new.dat") + " system.img" + o)
        show("Extracting vendor.img ...")
        os.system("sudo python2 /etc/liteapplication/rom-unzip/sdat2img.py " + path("vendor.transfer.list") + " " + path("vendor.new.dat") + " vendor.img" + o)
    def save_img(self):
        if not args.extract in os.getcwd():
            os.chdir(os.path.realpath(args.extract))
        show("Mounting system.img ...")
        os.system("mkdir system.dir")
        os.system("sudo mount -t ext4 -o loop system.img system.dir/")
        show("Mounting vendor.img ...")
        os.system("mkdir vendor.dir")
        os.system("sudo mount -t ext4 -o loop vendor.img vendor.dir/")
        unnecessary_files = ["system.new.dat.br","system.new.dat","system.transfer.list","system.patch.dat","vendor.new.dat.br","vendor.new.dat","vendor.transfer.list","vendor.patch.dat"]
        for file in unnecessary_files:
            if os.path.exists(file):
                os.remove(file)
                show("Removed '{}'".format(file))
        if os.path.isdir("./system"):
            shutil.rmtree("./system")
            show("Removed system unnecessary folder")
        if os.path.isdir("./vendor"):
            shutil.rmtree("./vendor")
            show("Removed vendor unnecessary folder")
        os.system("sudo nautilus " + os.getcwd() + " &")
        show("Run 'sudo rom-unzip -U' to unmount. ")
    def umount(self):
        os.system("sudo umount {}/system.dir".format(args.extract))
        os.system("sudo umount {}/vendor.dir".format(args.extract))
        os.rmdir("{}/system.dir".format(args.extract))
        os.rmdir("{}/vendor.dir".format(args.extract))
    def set_state(self, state, dest):
        if not os.path.exists(dest+"/.state.save"):
            os.mknod(dest+"/.state.save")
        content = [str(state),"\n",str(self.rom)]
        with open(dest+"/.state.save","w") as f:
            f.writelines(content)
    def get_state(self, dest):
        with open(dest+"/.state.save","r+") as f:
            return str(f.readlines()[0])

def show(message):
    if args.verbose or args.log != "none":
        time_act = round( time.time() - start_time, 2 )
        mem_act = round( memory_profiler.memory_usage()[0] - start_memory[0], 2 )
        message="[ EXEC = {}s , MEM = {}MB ]\t {}".format(time_act,mem_act,message)
        if args.verbose:
            print(message)
        if args.log != "none":
            with open(args.log,'a') as l:
                l.write(message + "\r\n")
def path(s):
    return os.path.abspath(glob.glob(s)[0])
def root():
    if os.geteuid() != 0:
        print("Please run this script as root\nwith 'sudo "+sys.argv[0]+"'")
        print("CODE : 1")
        exit(1)
try:
    last = float(urllib.request.urlopen("https://raw.githubusercontent.com/LiteApplication/rom-unzip/master/src/version").readline())
    if float(rom_unzip.__version__) < float(last) and not args.no_update:
        show("A new version of rom-unzip is available, updating ...")
        root()
        os.system("curl -s https://raw.githubusercontent.com/LiteApplication/rom-unzip/master/install | sudo bash > /dev/null")
        show("Done. ")
        os.execv(__file__, sys.argv)
except:
    show("Cannot check for update")
try:
    show("Rom-unzip by LiteApplication v" + str(rom_unzip.__version__))
    ru = rom_unzip()
    tb = rom_toolbox()
    if args.version:
        print("Rom-unzip by LiteApplication v" + str(rom_unzip.__version__))
        exit(0)
    elif args.update:
        show("Updating ...")
        root()
        os.system("curl -s https://raw.githubusercontent.com/LiteApplication/rom-unzip/master/install | sudo bash")
        exit(0)
    elif args.umount:
        show("Unmounting system and vendor, 'sudo rom-unzip -m 7' to reverse. ")
        root()
        ru.umount()
        exit(0)
    if args.resume:
        root()
        ru.resume()
    elif int(args.step) > -1 and int(args.step) <= 8:
        root()
        ru.run_step(args.step)
    elif int(args.step) <= -1 and int(args.step) > 9:
        root()
        ru.run_all()
    elif args.saved:
        print(ru.get_state(args.extract))
    elif args.all:
        root()
        ru.run_all()
except KeyboardInterrupt:
    show("Exiting...")
    exit(0)
