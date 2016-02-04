import logging
import sys, os, getopt, tempfile, subprocess
import sqlite3

from PIL import Image
from PIL.ExifTags import TAGS

import defaults

import matching
from matching import *

import features
from features import *

# a helper function to get list of photos from a directory
def getPhotosFromDirectory(photoDir):
    return [f for f in os.listdir(photoDir) if os.path.isfile(os.path.join(photoDir, f)) and os.path.splitext(f)[1].lower()==".jpg"]


distrPath = os.path.dirname( os.path.abspath(sys.argv[0]) )
bundlerExecutable = ''
if sys.platform == "win32": bundlerExecutable = os.path.join(distrPath, "software/bundler/bin/bundler.exe")
else: bundlerExecutable = os.path.join(distrPath, "software/bundler/bin/bundler")

SCALE = 1.0
bundlerListFileName = "list.txt"

camerasDatabase = os.path.join(distrPath, "osmbundler/cameras/cameras.sqlite")
commandLineLongFlags = [
"photos=",
"maxPhotoDimension=",
"featureExtractor=",
"photoScalingFactor=",
"checkCameraDatabase"
]
exifAttrs = set(["Model", "Make", "ExifImageWidth", "ExifImageHeight", "FocalLength"])

class ZeroValueException(Exception):
    """Raised if zero value has been encountered
    Used to process user input
    """


class OsmBundler():

    currentDir = ""

    workDir = ""
    
    # value of command line argument --photos=<..>
    photosArg = ""
    
    featureExtractor = None
    
    matchingEngine = None
    
    # sqlite cursor
    dbCursor = None
    
    # list of photos with focal distances for bundler input
    bundlerListFile = None
    
    # list of files with extracted features
    featuresListFile = None
    
    # information about each processed photo is stored in the following dictionary
    # photo file name in self.workDir is used as the key in this dictionary
    photoDict = {}
    
    featureExtractionNeeded = True
    
    photoScalingFactor = 0

    def __init__(self):
        for attr in dir(defaults):
            if attr[0]!='_':
                setattr(self, attr, getattr(defaults, attr))
        
        self.parseCommandLineFlags()

        # save current directory (i.e. from where RunBundler.py is called)
        self.currentDir = os.getcwd()
        # create a working directory
        self.workDir = tempfile.mkdtemp(prefix="osm-bundler-")
        logging.info("Working directory created: "+self.workDir)
        
        if not (os.path.isdir(self.photosArg) or os.path.isfile(self.photosArg)):
            raise Exception, "'%s' is neither directory nor a file name" % self.photosArg
        
        # initialize mathing engine based on command line arguments
        self.initMatchingEngine()

        # initialize feature extractor based on command line arguments
        self.initFeatureExtractor()

    def parseCommandLineFlags(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "", commandLineLongFlags)
        except getopt.GetoptError:
            self.printHelpExit()

        for opt,val in opts:
            opt = opt[2:]
            if opt=="photos":
                self.photosArg = val
            elif opt=="maxPhotoDimension":
                if val.isdigit() and int(val)>0: self.maxPhotoDimension = int(val)
            elif opt=="photoScalingFactor":
                try:
                    val = float(val)
                    if val>0 and val<=1: self.photoScalingFactor = val
                except:
                    # do nothing
                    pass
            elif opt=="matchingEngine":
                self.matchingEngine = val
            elif opt=="featureExtractor":
                self.featureExtractor = val
            elif opt=="checkCameraDatabase":
                if not self.photosArg:
                    try:
                        self.photosArg = opt["--photos"]
                    except:
                        self.printHelpExit()
                self.checkCamerasInDatabase()
                sys.exit(2)
            elif opt=="help":
                self.printHelpExit()
        
        if self.photosArg=="": self.printHelpExit()

    def preparePhotos(self, *kargs, **kwargs):
        # open each photo, resize, convert to pgm, copy it to self.workDir and calculate focal distance
        # conversion to pgm is performed by PIL library
        # EXIF reading is performed by PIL library
        
        # open connection to cameras database
        conn = sqlite3.connect(camerasDatabase)
        self.dbCursor = conn.cursor()
        
        # open list of photos with focal distances for bundler input
        self.bundlerListFile = open(os.path.join(self.workDir,bundlerListFileName), "w")

        # check if need to do feature extraction
        if ('featureExtractionNeeded' in kwargs and kwargs['featureExtractionNeeded']==False) or self.matchingEngine.featureExtractionNeeded==False:
            self.featureExtractionNeeded = False
        elif self.matchingEngine.featureExtractionNeeded:
            # open list of files with extracted features
            self.featuresListFile = open(os.path.join(self.workDir,self.matchingEngine.featuresListFileName), "w")

        if os.path.isdir(self.photosArg):
            # directory with images
            photos = getPhotosFromDirectory(self.photosArg)
            if len(photos)<3: raise Exception, "The directory with images should contain at least 3 .jpg photos"
            for photo in photos:
                photoInfo = dict(dirname=self.photosArg, basename=photo)
                self._preparePhoto(photoInfo)
        elif os.path.isfile(self.photosArg):
            # a file with a list of images
            photosFile = open(self.photosArg)
            # an auxiliary dictionary to eliminate duplicated photos
            _photoDict = {}
            for photo in photosFile:
                photo = photo.rstrip()
                if os.path.isfile(photo):
                    if not photo in _photoDict:
                        _photoDict[photo] = True
                        dirname,basename = os.path.split(photo)
                        photoInfo = dict(dirname=dirname, basename=basename)
                        self._preparePhoto(photoInfo)
            photosFile.close()

        if self.featuresListFile: self.featuresListFile.close()
        self.bundlerListFile.close()
        self.dbCursor.close()


    def checkCamerasInDatabase(self):
        # open connection to cameras database
        conn = sqlite3.connect(camerasDatabase)
        self.dbCursor = conn.cursor()
    
        if os.path.isdir(self.photosArg):
            # directory with images
            photos = getPhotosFromDirectory(self.photosArg)
            for photo in photos:
                self.checkCameraInDatabase( os.path.join(self.photosArg, photo) )
        elif os.path.isfile(self.photosArg):
            # a file with a list of images
            photosFile = open(self.photosArg)
            for photo in photosFile:
                photo = photo.rstrip()
                if os.path.isfile(photo):
                    self.checkCameraInDatabase(photo)
            photosFile.close()

        conn.commit()
        self.dbCursor.close()


    def checkCameraInDatabase(self, photoPath):
        photoHandle = Image.open(photoPath)
        exif = self._getExif(photoHandle)
        if 'Make' in exif and 'Model' in exif:
            exifMake = exif['Make'].strip()
            exifModel = exif['Model'].strip()
            ccdWidth = self.getCcdWidthFromDatabase(exifMake, exifModel)
            if ccdWidth==None:
                while True:
                    print "Type CCD width in mm for the camera %s, %s. Press Enter to skip the camera." % (exifMake, exifModel)
                    userInput = raw_input("CCD width in mm: ")
                    # Enter key was pressed
                    if not userInput: return
                    try:
                        ccdWidth = float(userInput)
                        if ccdWidth==0: raise ZeroValueException
                        self.dbCursor.execute("insert into cameras(make, model, ccd_width, source) values(?, ?, ?, 2)", (exifMake, exifModel, ccdWidth))
                    except ZeroValueException:
                        print "\nCCD width can not be equal to zero."
                    except ValueError:
                        print "\nIncorrect value for the CCD width. Please enter CCD width in mm."
                    except:
                        print "\nCan not insert CCD width to the database."
                    else:
                        print "CCD width %s for the cameras %s,%s has been successively inserted to the database" % (ccdWidth, exifMake, exifModel)
                        return
	    else:
		print "Camera is already inserted into the database"
                return
                
    def _preparePhoto(self, photoInfo):
        photo = photoInfo['basename']
        photoDir = photoInfo['dirname']
        logging.info("\nProcessing photo '%s':" % photo)
        inputFileName = os.path.join(photoDir, photo)
        photo = self._getPhotoCopyName(photo)
        outputFileNameJpg = "%s.jpg" % os.path.join(self.workDir, photo)
        # open photo
        photoHandle = Image.open(inputFileName)
        # get EXIF information as a dictionary
        exif = self._getExif(photoHandle)
        self._calculateFocalDistance(photo, photoInfo, exif)
        
        # resize photo if necessary
        # self.photoScalingFactor takes precedence over self.maxPhotoDimension
        scale = 0
        if self.photoScalingFactor: scale = self.photoScalingFactor
        else:
            maxDimension = photoHandle.size[0]
            if photoHandle.size[1]>maxDimension: maxDimension = photoHandle.size[1]
            if maxDimension > self.maxPhotoDimension: scale = float(self.maxPhotoDimension)/float(maxDimension)
        if scale > 0:
            newWidth = int(scale * photoHandle.size[0])
            newHeight = int(scale * photoHandle.size[1])
            photoHandle = photoHandle.resize((newWidth, newHeight))
            logging.info("\tCopy of the photo has been scaled down to %sx%s" % (newWidth,newHeight))
        
        photoInfo['width'] = photoHandle.size[0]
        photoInfo['height'] = photoHandle.size[1]
        
        photoHandle.save(outputFileNameJpg)
        
        # put photoInfo to self.photoDict
        self.photoDict[photo] = photoInfo

        if self.featureExtractionNeeded:
            outputFileNamePgm = "%s.pgm" % outputFileNameJpg
            photoHandle.convert("L").save(outputFileNamePgm)
            self.extractFeatures(photo)
            os.remove(outputFileNamePgm)


    def _getPhotoCopyName(self, photo):
        # cut off the extension
        photo = photo[:-4]
        # replace spaces in the file name
        photo = photo.replace(' ', '_')
        # find a unique name
        suffix = 1
        while photo in self.photoDict:
            photo = "%s_%s" % (photo, suffix)
            suffix = suffix + 1
        return photo


    def _getExif(self, photoHandle):
        exif = {}
        info = photoHandle._getexif()
        if info:
            for attr, value in info.items():
                decodedAttr = TAGS.get(attr, attr)
                if decodedAttr in exifAttrs: exif[decodedAttr] = value
        if 'FocalLength' in exif: exif['FocalLength'] = float(exif['FocalLength'][0])/float(exif['FocalLength'][1])
        return exif
    
    def _calculateFocalDistance(self, photo, photoInfo, exif):
        hasFocal = False
        if 'Make' in exif and 'Model' in exif:
            # check if we have camera entry in the database
            ccdWidth = self.getCcdWidthFromDatabase(exif['Make'].strip(),exif['Model'].strip())
            if ccdWidth:
                if 'FocalLength' in exif and 'ExifImageWidth' in exif and 'ExifImageHeight' in exif:
                    focalLength = float(exif['FocalLength'])
                    width = float(exif['ExifImageWidth'])
                    height = float(exif['ExifImageHeight'])
                    if focalLength>0 and width>0 and height>0:
                        if width<height: width = height
                        focalPixels = width * (focalLength / ccdWidth[0])
                        hasFocal = True
                        self.bundlerListFile.write("%s.jpg 0 %s\n" % (photo,SCALE*focalPixels))
            else: logging.info("\tEntry for the camera '%s', '%s' does not exist in the camera database" % (exif['Make'], exif['Model']))
        if not hasFocal:
            logging.info("\tCan't estimate focal length in pixels for the photo '%s'" % os.path.join(photoInfo['dirname'],photoInfo['basename']))
            self.bundlerListFile.writelines("%s.jpg\n" % photo)


    def initMatchingEngine(self):
        try:
            matchingEngine = getattr(matching, self.matchingEngine)
            matchingEngineClass = getattr(matchingEngine, matchingEngine.className)
            self.matchingEngine = matchingEngineClass(os.path.join(distrPath, "software"))
        except:
            raise Exception, "Unable initialize matching engine %s" % self.featureExtractor

    def initFeatureExtractor(self):
        try:
            featureExtractor = getattr(features, self.featureExtractor)
            featureExtractorClass = getattr(featureExtractor, featureExtractor.className)
            self.featureExtractor = featureExtractorClass(os.path.join(distrPath, "software"))
        except:
            raise Exception, "Unable initialize feature extractor %s" % self.featureExtractor

    def extractFeatures(self, photo):
        # let self.featureExtractor do its job
        os.chdir(self.workDir)
        self.featureExtractor.extract(photo, self.photoDict[photo])
        self.featuresListFile.write("%s.%s\n" % (photo, self.featureExtractor.fileExtension))
        os.chdir(self.currentDir)
    
    def matchFeatures(self):
        # let self.matchingEngine do its job
        os.chdir(self.workDir)
        self.matchingEngine.match()
        os.chdir(self.currentDir)

    
    def doBundleAdjustment(self):
        # just run Bundler here
        logging.info("\nPerforming bundle adjustment...")
        os.chdir(self.workDir)
        os.mkdir("bundle")
        
        # create options.txt
        optionsFile = open("options.txt", "w")
        optionsFile.writelines(defaults.bundlerOptions)
        optionsFile.close()

        bundlerOutputFile = open("bundle/out", "w")
        subprocess.call([bundlerExecutable, "list.txt", "--options_file", "options.txt"], **dict(stdout=bundlerOutputFile))
        bundlerOutputFile.close()
        os.chdir(self.currentDir)
        logging.info("Finished! See the results in the '%s' directory" % self.workDir)
    
    def printHelpExit(self):
        self.printHelp()
        sys.exit(2)
    
    def openResult(self):
        if sys.platform == "win32": subprocess.call(["explorer", self.workDir])
	if sys.platform == "linux2": subprocess.call(["xdg-open", self.workDir])
        else: print "Thanks"
    
    def printHelp(self):
        helpFile = open(os.path.join(distrPath, "osmbundler/help.txt"), "r")
        print helpFile.read()
        helpFile.close()

    # a helper function to get CCD width from sqlite database
    def getCcdWidthFromDatabase(self, exifMake, exifModel):
        self.dbCursor.execute("select ccd_width from cameras where make=? and model=?", (exifMake, exifModel))
        return self.dbCursor.fetchone()


# service function: get path of an executable (.exe suffix is added if we are on Windows)
def getExecPath(dir, fileName):
    if sys.platform == "win32": fileName = "%s.exe" % fileName
    return os.path.join(dir, fileName)
