
         Demo code for detecting and matching SIFT features
         --------------------------------------------------
                    David Lowe (lowe@cs.ubc.ca)
                     Version 4, July 6, 2005


This directory contains compiled binary programs for finding SIFT
invariant features that can run under Linux or Windows.  In addition,
there is a Matlab script as well as C source code showing how to load
the features and do simple feature matching.

See the web page at 
  http://www.cs.ubc.ca/~lowe/keypoints/ 
for references to the relevant papers describing this approach.


Running from within Matlab
--------------------------

If you have access to Matlab, scripts are provided for loading SIFT
features and finding matches between images.  These were tested under
Matlab Version 7 and do not require the image processing toolbox.

Run Matlab in the current directory and execute the following
commands.  The "sift" command calls the appropriate binary to extract
SIFT features (under Linux or Windows) and returns them in matrix
form.  Use "showkeys" to display the keypoints superimposed on the
image:

  [image, descrips, locs] = sift('scene.pgm');
  showkeys(image, locs);

The "match" command is given two image file names.  It extracts SIFT
features from each image, matches the features between the two images,
and displays the results.

  match('scene.pgm','book.pgm');

The result shows the two input images next to each other, with lines
connecting the matching locations.  Most of the matches should be
correct (as can be roughly judged by the fact that they select the
correct object in a cluttered image), but there will be a few false
outliers that could be removed by enforcing viewpoint consistency
constraints.

You can also try matching other images:

  match('scene.pgm','box.pgm');
  match('scene.pgm','basmati.pgm');

For more details, see the comments in the Matlab scripts: sift.m,
showkeys.m, and match.m.

Acknowledgments: The Matlab script for loading SIFT features is based
on one provided by D. Alvaro and J.J. Guerrero.


Binaries for detecting SIFT features
------------------------------------

You do not need Matlab to run the demo.  The program binary for
keypoint extraction under Linux is named "sift", and should run under
most versions of Linux on Intel compatible processors.  The executable
for Windows is named "siftWin32.exe".  The code was developed under
Linux and follows Unix conventions, but the Windows binary produces
identical keypoints.

You can detect keypoints and display them on the provided test images
with the command line option "-display" as follows (for Linux):

% sift -display <book.pgm >result.pgm

[If you are using Windows, first open the Windows Command Prompt and
cd to the directory containing the binary before executing the
command.  In all cases when using Windows, replace sift with
siftWin32.]

This will write out a new image, result.pgm, with arrows overlayed
indicating the locations, scales, and orientations of the key
features.  You can inspect this image using the public domain program xv:

% xv result.pgm

or use any other tool that displays the common PGM image format.  

[Under Windows, you can use the freeware program IrfanView (www.irfanview.com)
to view PGM images and covert to/from other formats.]

Note that you can control the number of keypoints by scaling the image
resolution.  An image of size 500 pixels square will typically give
over 1000 keypoints depending on image content, which is plenty for
most applications.  Images from most digital cameras should be greatly
reduced in resolution before being used.  Changing image resolution is
the best method to control the number of keypoints, as it is the
larger scale keypoints that are most reliable and this is also much
more efficient than processing large images.  The current compiled
binaries will raise an exception for images with dimensions greater
than about 1800 pixels in any dimension.  Color images will need to
be convereted to grayscale (PGM format is only for grayscale images).


ASCII file output for keypoints
-------------------------------

Without any command line arguments, the "keypoint" program will
output the keypoints in a simple ASCII file format that
is convenient to read by other programs and provides the data needed
for matching keypoints:

% sift <book.pgm >book.key

The file format starts with 2 integers giving the total number of
keypoints and the length of the descriptor vector for each keypoint
(128). Then the location of each keypoint in the image is specified by
4 floating point numbers giving subpixel row and column location,
scale, and orientation (in radians from -PI to PI).  Obviously, these
numbers are not invariant to viewpoint, but can be used in later
stages of processing to check for geometric consistency among matches.
Finally, the invariant descriptor vector for the keypoint is given as
a list of 128 integers in range [0,255].  Keypoints from a new image
can be matched to those from previous images by simply looking for the
descriptor vector with closest Euclidean distance among all vectors
from previous images.


Example of image matching using keypoints
-----------------------------------------

To demonstrate the value of the keypoints for image matching, this
directory also contains some simple C source code to read keypoints from
2 images and show the best matches between the images with lines drawn
on top of the images connecting the matching locations.  The code is
written for Linux, although it should not be difficult to port to Windows.

The matches are identified by finding the 2 nearest neighbors of each
keypoint from the first image among those in the second image, and
only accepting a match if the distance to the closest neighbor is less
than 0.6 of that to the second closest neighbor.  The threshold of 0.6
can be adjusted up to select more matches or down to select only the
most reliable.  See my research papers for the justification behind
this approach.

First, create keypoints for each test image:

% sift <book.pgm >book.key
% sift <scene.pgm >scene.key

To compile the matching code in this directory under Linux, simply do:
% make

[No makefile is given for Windows, although the code is quite portable
and should be fairly easy to compile under Windows.]

This will create a demo program called "match".  This program
requires command line arguments giving each of the two images and
their corresponding keypoints:

% match -im1 book.pgm -k1 book.key -im2 scene.pgm -k2 scene.key > out.pgm

The resulting image in "out.pgm" contains the first image above the
second one, with white lines connecting the matching locations.  Most
of the matches should be correct (as can be roughly judged by the fact
that they select the correct object in a cluttered image), but there
will be a few false outliers that could be removed by enforcing
viewpoint consistency constraints.  You can inspect the matching
results with xv:

% xv out.pgm

You can also try the results for the other objects in the scene:

% sift <box.pgm >box.key
% match -im1 box.pgm -k1 box.key -im2 scene.pgm -k2 scene.key > out.pgm
% sift <basmati.pgm >basmati.key
% match -im1 basmati.pgm -k1 basmati.key -im2 scene.pgm -k2 scene.key > out.pgm

You should be able to run this demo program to find matches between
any pair of images in PGM format.  Of course, this matching approach
is overly simple, and many more correct matches could be found by
using a higher distance threshold and enforcing viewpoint consistency
constraints between the set of resulting matches to eliminate
outliers, as described in my research papers.


Licensing conditions
--------------------

This software is being made available for research purposes only.  It
is necessary to obtain a license from the University of British
Columbia for commercial applications.  See the file LICENSE in this
directory for conditions of use.

