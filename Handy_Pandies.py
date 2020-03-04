"""
TUDublin School of Electrical and Electronic Engineering
DT021A/4 Image Processing
Group Project: Handy Pandies
Authors: Peter Kinsella, Stephen Sheridan, Su Ye Shan Daniel
Lecturer Dr. Jane Courtney
Last Updated: 23-11-2019


****************     Introduction    ****************

The aim for this project was to locate a hand in an image and determine if the hand was in the form on an "ok" sign or
otherwise. This project evolved gradually as each week our knowledge and understanding of image processing tools grew.
After trialling a number of techniques such as the Hough Circle gradient, differing colour spaces and shape finding
algorithms the code was finally simplified using thresholds, contours and blob detection. Having found relative success
with static images it was decided to push a bit further and try work with video.


****************     The process      ****************
The finished code uses the following steps.

1. Load in a video of a hand frame by frame, each frame wil be processed as an image the same way
2. Resize the image down to a manageable size
3. Convert the image to gray scale, use a gaussian blur to average out the values and then threshold the image.
4. Perform a boundary gradient of the threshold to get a good border to work with.
5. Get the contours of the boundary
6. Create a simple blob detector using different tested parameters
7. Use the blob detector to locate the hole in the hand
8. Draw a circle around the located blob and print it onto the original image
9. Locate the largest contour by area, save it and hull it
10. Get the center moment of the largest contour and indicate it on the image with a small circle
11. Display the contours and hull on the original image as well to show the location of the hand
12. Save the frames as a final video

****************     Conclusions      ****************

Overall the code works relatively well, the algorithm is able to detect the hand gesture and this could obviously then
be used to isolate the hand for further processing. It was found in testing however that some background colours gave
false positives as the threshold is not as sophisticated as it could be. In future the next step would be to optimise the
thresholds for the hands to obtain more reliable results regardless of where the hand is placed.
Regarding the use of video, this was initially tested using live video from a webcam. While the code worked well detecting
the region of interest on the fly, it was rather slow and jumpy. Obviously this would require further optimisation and
refinement to be practical.

Further development of the code would likely involve defect detection to recognise a broad range of hand gestures with
the ultimate goal being to read sign language.

****************     References     ****************

[1] Towhid, N. (2019). openCV video saving in python. [online] Stack Overflow.
    Available at: https://stackoverflow.com/questions/29317262/opencv-video-saving-in-python [Accessed 21 Nov. 2019].

[2] Consulting, A. (2019). Blob Detection Using OpenCV ( Python, C++ ) | Learn OpenCV. [online] Learnopencv.com.
    Available at: https://www.learnopencv.com/blob-detection-using-opencv-python-c/ [Accessed 18 Nov. 2019].

[3] Creat-tabu.blogspot.com. (2019). Opencv python hand gesture recognition.
    [online] Available at: http://creat-tabu.blogspot.com/2013/08/opencv-python-hand-gesture-recognition.html
    [Accessed 18 Nov. 2019].



"""


import numpy as np
import cv2

vc = cv2.VideoCapture("final2.mp4") # video capture [1]

out = cv2.VideoWriter('output.mp4', -1, 20.0, (640,480))

rval , frame = vc.read()

while True:

  if frame is not None:

    rval, frame = vc.read()

  else:
      break

  shape = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))

  dim = (600, 400) # resizing image

  resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

  gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
  blur = cv2.GaussianBlur(gray, (5, 5), 0)
  ret, thresh = cv2.threshold(blur, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
  boundary = cv2.morphologyEx(thresh, cv2.MORPH_GRADIENT, shape)

  contours, hierarchy = cv2.findContours(boundary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  drawing = np.zeros(resized.shape, np.uint8)

  # Setup SimpleBlobDetector parameters [2]
  params = cv2.SimpleBlobDetector_Params()

  params.filterByArea = True
  params.minArea = 1000
  params.filterByCircularity = True
  params.minCircularity = 0.6
  params.filterByConvexity = True
  params.minConvexity = 0.6
  params.filterByInertia = True
  params.minInertiaRatio = 0.3

  detector = cv2.SimpleBlobDetector_create(params)

  # Detect blobs.
  blobs = detector.detect(boundary)

  # Draws circles around blobs and prints onto original image
  image_blobs = cv2.drawKeypoints(resized, blobs, np.array([]), (0, 0, 255),
                                  cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

  max_area = 0
  for i in range(len(contours)): # finding largest contour by area [3]
      contour = contours[i]
      area = cv2.contourArea(contour)
      if (area > max_area):
          max_area = area
          ci = i
  contour = contours[ci]
  hull = cv2.convexHull(contour)
  moments = cv2.moments(contour)
  if moments['m00'] != 0:  # this gives the centre of the moments [3]
      cx = int(moments['m10'] / moments['m00'])  # cx = M10/M00
      cy = int(moments['m01'] / moments['m00'])  # cy = M01/M00

  center = (cx, cy)
  cv2.circle(image_blobs, center, 5, [0, 0, 255], 2)  # draws small circle at the center moment
  cv2.drawContours(image_blobs, [contour], 0, (0, 255, 0), 2)
  cv2.drawContours(image_blobs, [hull], 0, (0, 0, 255), 2)

  out.write(image_blobs)
  cv2.imshow("preview", image_blobs)

  if cv2.waitKey(1) & 0xFF == ord('q'):
     break

vc.release()
out.release() # saving video

