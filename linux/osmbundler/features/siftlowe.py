import os, subprocess, gzip

from sift import Sift

className = "LoweSift"
class LoweSift(Sift):
    
    win32Executable = "sift-lowe/siftWin32.exe"
    linuxExecutable = "sift-lowe/sift"
    
    def __init__(self, distrDir):
        Sift.__init__(self, distrDir)

    def extract(self, photo, photoInfo):
        photoFile = open("%s.jpg.pgm" % photo, "rb")
        siftTextFile = open("%s.key" % photo, "w")
        subprocess.call(self.executable, **dict(stdin=photoFile, stdout=siftTextFile))
        photoFile.close()
        siftTextFile.close()
        # gzip SIFT file and remove it
        siftTextFile = open("%s.key" % photo, "r")
        siftGzipFile = gzip.open("%s.key.gz" % photo, "wb")
        siftGzipFile.writelines(siftTextFile)
        siftGzipFile.close()
        siftTextFile.close()
        os.remove("%s.key" % photo)