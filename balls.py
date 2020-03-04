""" Stephen Sheridan C16746195 DT021A/4
November 17 2019
Lecturer: Dr Jane Courtney

#######  Image processing 'SpotTheBall' assignment  ########


#######  introduction  ########

The code below attempts to remove the white ball from the image and disguise the original location. A number of
approaches were tested to improve the ball detecting capabilities however the final script is relatively simple and
relies on techniques learned in the image processing module. The strongest part of the script is the detection,
this has been tested on a number of images other than those supplied and appears to work well. The ball removal
section however still has room for improvement, in some cases there are artefacts of the ball left. A workaround for
this is detailed in the instructions however it would be preferable to have it automated.

#######  Instructions  ########

simply run the script to operate.
To counteract the issue of artefacts, the first variable (art) declared should be adjusted. This alters the radius of the
selected region of interest. Increasing this value helps when the ball is large however it should be decreased if the
ball is close to another object. The default setting is 4. Images used for testing have been included.


####### Operation of the script ########

To begin the script converts the image to the RGB colour space. It was found through investigation that this was the
most suitable colour space for the project as it offered the best isolation for the region of interest.
The  values for the pixels of each channel where the ball sat were noted and then used to set the thresholds.
This in turn isolated the ball and other white objects.

The next step is morphology. By opening the image most items that are not within the region of interest
are removed. This reduces the occurrence of false positives.

Following the morphology, the findContours function is utilised. This outputs a vector of vectors that is then ordered
by size, the assumption being that the largest contour would be the ball. The centre and effective diameter of the
contour are then found.

Using the location data from the contours, the left half of the ball is erased using the pixels to the left of the ball
and similarly on the right.

####### Conclusions and suggested improvements ########
The script works quite well for finding the ball and isolating the region of interest. A proper circle finding
algorithm may work better however those tried seemed to fail on the golf ball as half of it is obscured by
grass. The in fill of the ball could definitely be improved, there is an inpaint function however it has a tendency to
lose the details. Given more time I would try to soften the edge of the cloned area and perhaps put in a user
prompt to choose the most suitable are to be cloned. This would help particularly in the case of the snooker ball
where the script really struggles.


####### References ########

[1] Alexander Mordvintsev & Abid Kl. (2013).'Contour Properties'' [Online]. Available:
https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_properties/py_contour_properties.html

[2] OpenCV.org (Date unknown).'Contour Features'' [Online]. Available:
https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html
"""

######## Begin code ########

import numpy as np
import cv2
from matplotlib import pyplot as plt
import easygui

######### If the ball is not completely removed, artefacts are left then increase the following variable #########
art=5
import sys
print(sys.version)
import cv2

######### Reading Images and setting up the colour spaces #########

# f = easygui.fileopenbox()
# I = cv2.imread(f)
I = cv2.imread('snooker.jpg')
RGB = cv2.cvtColor(I, cv2.COLOR_BGR2RGB)
G = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)

######### Setting the thresholds to help isolate the ball #########

RangeLower=(170,150,200)
RangeUpper=(255,255,255)
B =cv2.inRange(RGB,RangeLower,RangeUpper)

######### Performing morphology #########

shape = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(8,8))
D= cv2.morphologyEx(B,cv2.MORPH_OPEN,shape)

######### Finding the contours #########

(cnts, _) = cv2.findContours(D.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
c = max(cnts, key = cv2.contourArea)

######### Finding the centre of the contour [1] #########

M = cv2.moments(c)
cx = int(M["m10"] / M["m00"])
cy = int(M["m01"] / M["m00"])

######### Finding the diameter of the contour [2] #########

area = cv2.contourArea(c)
diameter = np.sqrt(art*area/np.pi)
dia=int(round(diameter))
dia2=int(round(diameter)*2)
rad=int(round(diameter/2))

######### Cloning the surrounding area to cover the ball #########

RGB[cy-rad:cy+dia2, cx-dia:cx]=RGB[cy-rad:cy+dia2, cx-dia2:cx-dia]
RGB[cy-rad:cy+dia2, cx:cx+dia]=RGB[cy-rad:cy+dia2, cx+dia:cx+dia2]

plt.imshow(RGB)
plt.show()

"""

"""