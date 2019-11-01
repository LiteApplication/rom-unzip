#!/usr/bin/python3
def main(runDir="NoDir"):
    try:
        import glob
        import os
        import zipfile
    except ImportError:
        print("Import Error : some modules can not be load, \nPlease check you run on Linux with glob and zipfile installed")
    try:
        srcPath=os.path.dirname(os.path.realpath(__file__))
    except NameError:
        print("Warning : please run this script from file. ")
        path=getcwd()
    if os.geteuid() != 0:
        print("Please run this script as root\nwith 'sudo "+sys.argv[0]+"'")
        print("CODE : 1")
        exit(1)
    if runDir=="NoDir":
        if len(sys.argv)==2:
            rundir=sys.argv[1]
        else:
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
        print("Multiple ROMs are available in this dirrectory : "
        rom=chooseFile(availableRom)
    elif len(availablerom)==0:
        print("Error : No rom available\nPlease cd to the rom.zip directory or use "+sys.argv[0]+" <directory>")
        print("CODE : 2")
        exit(2)
    else:
        rom=availableRom[0]
    os.system("srcPath+"romExtractor.sh", runDir+"/"+rom, srcPath)
def chooseFile(files):
    for i,file in zip(range(1,len(files)),files):
        print("\t"+i+" : "+file)
    print("\n\t0 : Exit")
    choice = int(input("Your choice : "))-1
    if choice == -1:
        print("Exiting...")
        print("CODE : 0")
        exit(0)
    else:
        return files[choice]
