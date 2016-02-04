---------------------------------------
WHAT IS PYTHON PHOTOGRAMMETRY TOOLBOX?
---------------------------------------

This project intend to create a python photogrammetry toolbox.
It provides an easy interface to run Bundler + Dense point cloud computation via PMVS2 and CMVS (as WIP).

The main drawbacks of Bundler is that people have to install cygwin to use it and windows.
The advantage of Python is that the scripting langage is multiplatform, so the same code will be ok to run Bundler and the other tools on windows, linux and mac ! No more cygwin... installation.

This project make the Sift detector from VLFeat library works with Bundler. So the toolchain is OpenSource from A to Z. Other modules could be plug into because of the modularity approach that have been choosen.

In a near future we could think in integrate a SIFTGpu matcher into the toolchain.


---------------------------------------
HOW TO USE IT
---------------------------------------

Perform point cloud and camera calibration :
$ RunBundler.py --photos="./examples/MyPhotos" 

You could test various option... $ RunBundler.py

In a second step you could compute the dense 3D point cloud in one step if the dataset have a reasonable size.

$ RunPMVS.py --bundlerOutputPath="C:/temp/PreviousLineTempDirectoryPath" 

If you have a lot of images, it better to use CMVS cluster computation.
It performs dense 3D point could computation by using Cluster 3D representation of the scene :

$ RunCMVS.py --bundlerOutputPath="C:/temp/PreviousLineTempDirectoryPath" --ClusterToCompute ="Number of Desired Cluster".
Example :
$ RunCMVS.py --bundlerOutputPath="C:/temp/osm-Result" --ClusterToCompute ="10".


---------------------------------------
WHAT'S INCLUDED & LICENSE
---------------------------------------

Bundler > GNU General Public License
CMVS/PMVS2 > GNU General Public License
VLFeat > GNU General Public License
Python Photogrammetry Toolbox > GNU General Public License
Python Photogrammetry Toolbox GUI > GNU General Public License


---------------------------------------
LINKS
---------------------------------------

http://opensourcephotogrammetry.blogspot.com/2010/09/python-photogrammetry-toolbox.html
http://code.google.com/p/osm-bundler/w/list
