#!/usr/bin/python3
try:
    import glob
    import os
    import zipfile
except ImportError:
    print("Import Error : some modules can not be load, \nDo you have installed this with ./install ?")
    exit(1)
def select(runDir="NoDir"): #return a rom zip (absolute path) from runDir
    if os.geteuid() != 0:
        print("Please run this script as root\nwith 'sudo "+sys.argv[0]+"'")
        print("CODE : 1")
        exit(1)
    if runDir=="NoDir":
        runDir=os.getcwd()
    ROM_FILES=["META-INF/","system.new.dat.br","vendor.new.dat.br","system.transfer.list","vendor.transfer.list"]
    print("Finding ROM zip file...")
    availableZip=glob.glob(runDir+"/*.zip")
    availableRom=[]
    for zip in availableZip:
        zipf = zipfile.ZipFile(zip)
        if ROM_FILES in zip.namelist():
            availableRom.append(zip)
    if len(availableRom)<= 2:
        print("Multiple ROMs are available in this directory : ")
        rom=chooseFile(availableRom)
    elif len(availablerom)==0:
        return "NOROM"
    else:
        rom=availableRom[0]
    return rom
def unzip(source,path):
    print("Extracting rom files...")
    zipfile.ZipFile(source, 'r').extractall(path)
def unbr(source,path):
    os.system("brotli","-d",source,"--out",path)
def chooseFile(files):
    for i,file in zip(range(1,len(files)),files):
        print("\t"+i+" : "+os.path.splitext(os.path.basename(file)))[0]
    print("\n\t0 : Exit")
    choice = int(input("Your choice : "))-1
    if choice == -1:
        print("Exiting...")
        exit(0)
    else:
        return files[choice]
