import sys, os, logging

from extractor import FeatureExtractor

class Sift(FeatureExtractor):
    
    fileExtension = "key"
    
    executable = ''
    win32Executable = ''
    linuxExecutable = ''
    
    def __init__(self, distrDir):
        if sys.platform == "win32":
            self.executable = os.path.join(distrDir, self.win32Executable)
        else:
            self.executable = os.path.join(distrDir, self.linuxExecutable)
        logging.info("Sift executable path: %s" % self.executable)

    def extract(self, photo, photoInfo):
        pass