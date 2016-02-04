import logging
import sys, os, getopt, tempfile, subprocess, shutil

# service function: get path of an executable (.exe suffix is added if we are on Windows)
def getExecPath(dir, fileName):
    if sys.platform == "win32": fileName = "%s.exe" % fileName
    return os.path.join(dir, fileName)
    
distrPath = os.path.dirname( os.path.abspath(sys.argv[0]) )

pmvsExecutable = getExecPath(distrPath, "software/pmvs/bin/pmvs2")

bundlerBinPath = ''
if sys.platform == "win32": bundlerBinPath = os.path.join(distrPath, "software/bundler/bin/")
else: bundlerBinPath = os.path.join(distrPath, "software/bundler/bin/")

bundler2PmvsExecutable = getExecPath(bundlerBinPath, "Bundle2PMVS")
RadialUndistordExecutable = getExecPath(bundlerBinPath, "RadialUndistort")
Bundle2VisExecutable = getExecPath(bundlerBinPath, "Bundle2Vis")

bundlerListFileName = "list.txt"

commandLineLongFlags = ["bundlerOutputPath="]


class OsmPmvs():

    currentDir = ""

    workDir = ""
    
    # value of command line argument --bundlerOutputPath=<..>
    bundleOutArg = ""

    def __init__(self):
               
        self.parseCommandLineFlags()

        # save current directory (i.e. from where RunBundler.py is called)
        self.currentDir = os.getcwd()
        # create a working directory
        self.workDir = self.bundleOutArg
        logging.info("Working directory created: "+self.workDir)
        
        if not (os.path.isdir(self.bundleOutArg) or os.path.isfile(self.bundleOutArg)):
            raise Exception, "'%s' is neither directory nor a file name" % self.bundleOutArg

    def parseCommandLineFlags(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "", commandLineLongFlags)
        except getopt.GetoptError:
            self.printHelpExit()

        for opt,val in opts:
            if opt=="--bundlerOutputPath":
                self.bundleOutArg = val
            elif opt=="--help":
                self.printHelpExit()
        
        if self.bundleOutArg=="": self.printHelpExit()
    
    def doBundle2PMVS(self):
        # just run Bundle2PMVS here
        logging.info("\nPerforming Bundler2PMVS conversion...")
        os.chdir(self.workDir)
        os.mkdir("pmvs")

        # Create directory structure
        os.mkdir("pmvs/txt")
        os.mkdir("pmvs/visualize")
        os.mkdir("pmvs/models")
        
        #$BASE_PATH/bin32/Bundle2PMVS.exe list.txt  bundle/bundle.out
        print "Running Bundle2PMVS to generate geometry and converted camera file"
        subprocess.call([bundler2PmvsExecutable, "list.txt", "bundle/bundle.out"])
		
        # Apply radial undistortion to the images
        print "Running RadialUndistort to undistort input images"
        subprocess.call([RadialUndistordExecutable, "list.txt", "bundle/bundle.out", "pmvs"])
		
        print "Running Bundle2Vis to generate vis.dat"
        subprocess.call([Bundle2VisExecutable, "pmvs/bundle.rd.out", "pmvs/vis.dat"])

        os.chdir(os.path.join(self.workDir,"pmvs"))
        #Rename all the files to the correct name
        undistortTextFile = open("list.rd.txt", "r")
        imagesStrings = undistortTextFile.readlines()
        print "Move files in the correct directory"
        cpt = 0
        for imageString in imagesStrings:
          image = imageString.split(".")
          # sh => mv pmvs/et001.rd.jpg pmvs/visualize/00000000.jpg
          shutil.copy(image[0]+".rd.jpg", "visualize/%08d.jpg"%cpt)
          # sh => mv pmvs/00000000.txt pmvs/txt/
          shutil.copy("%08d.txt"%cpt, "txt/%08d.txt"%cpt)
          os.remove(image[0]+".rd.jpg")
          os.remove("%08d.txt"%cpt)
          cpt+=1
        
        undistortTextFile.close()
		
        logging.info("Finished!")
        
    def doPMVS(self):
        print "Run PMVS2 : %s " % pmvsExecutable
        subprocess.call([pmvsExecutable, "./", "pmvs_options.txt"])
	print "Finished! See the results in the '%s' directory" % self.workDir
	if sys.platform == "win32": subprocess.call(["explorer", self.workDir])
	if sys.platform == "linux2": subprocess.call(["xdg-open", self.workDir])
        else: print "Thanks"

    def printHelpExit(self):
        self.printHelp()
        sys.exit(2)
    
    def openResult(self):
        if sys.platform == "win32": subprocess.call(["explorer", self.workDir])
        else: print "See the results in the '%s' directory" % self.workDir
    
    def printHelp(self):
        print "Error"
        helpFile = open(os.path.join(distrPath, "osmpmvs/help.txt"), "r")
        print helpFile.read()
        helpFile.close()

