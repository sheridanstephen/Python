import numpy as np
import cv2
from matplotlib import pyplot as plt
from matplotlib import image as image
import easygui

""" 
#######  Image processing exam         #######  
#######  Stephen Sheridan C16746195    #######
#######  DT021A/4                      #######
#######  Lecturer Jane Courtney        #######

This code uses the blue channel to help isolate the ROI. 
It then finds the contours of the image and uses the cv2.minEnclosingCircle function
to calculate the length of the ruler.

Two approaches were tried to get the width. Firstly using corners, however it was difficult to tune. 
Secondly using the area of the contour. 
It runs well with the test image but has not been tested with other images.

#######  Instructions  ########

simply run the script to operate.
The rulers length in cm is set to 101cm. This can be changed via the first variable 'ruler'
To load a new image change the imread() value.

Have a nice day :)


"""
ruler=101


I=cv2.imread("Ruler.png")
I=cv2.cvtColor(I, cv2.COLOR_BGR2RGB) # Convert the image to rgb colour space
R,G,B = cv2.split(I)

dst = cv2.GaussianBlur(B, (5, 5), cv2.BORDER_DEFAULT)  # Blur, this helps the edge detection
E = cv2.Canny(dst, threshold1=10, threshold2=150)  # Edge detection

c, _ = cv2.findContours(E, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)  # Find the contours

c2 = sorted(c, key=cv2.contourArea, reverse=True) # Sort the contours by size (Largest first)
c3 = c2[0] # Choose the largest contour


((x, y), radius) = cv2.minEnclosingCircle(c3) # Find the minimum enclosing circle
center = (int(x), int(y))
cv2.circle(I,center,int(radius),(0,255,0),2)


pixPcm=(radius*2)/ruler # Calculate the Pixels per cm
ans=str(int(pixPcm))


# G = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
# corners =cv2.goodFeaturesToTrack(G,maxCorners=50, qualityLevel=0.9,minDistance=10) # Find the corners
# H =cv2.cornerHarris(G,blockSize=5,ksize=3,k=0.04)
#
# corners = np.int0(corners)
#
# for i in corners:
#     x,y = i.ravel()
#     cv2.circle(I,(x,y),3,(255,0,255),-1)




x, y, w, h = cv2.boundingRect(c3) # Calculate and draw the bounding rectangle
cv2.rectangle(I, (x, y), (x + w, y + h), (0, 0, 255), 2)

# ellipse =cv2.fitEllipse(c3)
# cv2.ellipse(I,ellipse, color=(0,255,0))

F =cv2.drawContours(I,c3,contourIdx=-1,color=(255,0,0),thickness=5) # Draw the largest contour in red

x,y,w,h = cv2.boundingRect(c3)

h2 = cv2.contourArea(c3)  # Calculate the area of the largest contour
h3=(h/(radius*2))*pixPcm # Calculate width of the ruler
h4=str(int(h3))


cv2.putText(I,"The ruler is" , (200,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),3) # Print the output on the image
cv2.putText(I,ans, (400,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),3)
cv2.putText(I,("pixels per cm" ), (470,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),3)
cv2.putText(I,"The height is",(200,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),3)
cv2.putText(I,h4,(430,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),3)
cv2.putText(I,"cm",(470,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),3)



plt.imshow(I) # Show the results
plt.show()



""""


    _                ___       _.--.
    \`.|\..----...-'`   `-._.-'_.-'`
    /  ' `         ,       __.--'
    )/' _/     \   `-_,   /
    `-'" `"\_  ,_.-;_.-\_ ',   
        _.-'_./   {_.'   ; /
       {_.-``-'         {_/
       
       
       
       
       """