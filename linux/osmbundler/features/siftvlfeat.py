import os, subprocess, gzip, logging

from sift import Sift

className = "VlfeatSift"
class VlfeatSift(Sift):
    
    win32Executable = "vlfeat/bin/w32/sift.exe"
    linuxExecutable = "vlfeat/bin/glx/sift"

    def __init__(self, distrDir):
        Sift.__init__(self, distrDir)

    def extract(self, photo, photoInfo):
        logging.info("\tExtracting features with the SIFT method from VLFeat library...")
        subprocess.call([self.executable, "%s.jpg.pgm" % photo, "-o", "%s.key" % photo])
        # perform conversion to David Lowe's format
        vlfeatTextFile = open("%s.key" % photo, "r")
        loweGzipFile = gzip.open("%s.key.gz" % photo, "wb")
        featureStrings = vlfeatTextFile.readlines()
        numFeatures = len(featureStrings)
        # write header
        loweGzipFile.write("%s 128\n" % numFeatures)
        for featureString in featureStrings:
            features = featureString.split()
            # swap features[0] and features[1]
            tmp = features[0]
            features[0] = features[1]
            features[1] = tmp
            i1 = 0
            for i2 in (4,24,44,64,84,104,124,132):
                loweGzipFile.write("%s\n" % " ".join(features[i1:i2]))
                i1 = i2
        loweGzipFile.close()
        vlfeatTextFile.close()
        # remove original SIFT file
        os.remove("%s.key" % photo)
        logging.info("\tFound %s features" % numFeatures)