import cv2
import matplotlib.pyplot as plt
import numpy as np

old = cv2.imread('/home/pi/Desktop/shot_output/0_shot.jpg')
new = cv2.imread('/home/pi/Desktop/shot_output/1_shot.jpg')

diff = cv2.absdiff(old, new)
print(diff.mean())


diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
diff = cv2.blur(diff, (10, 10)) # blur the image

ret, thresh = cv2.threshold(diff,50,255,0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

center_coords = []
for c in contours:
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    center_coords.append((cX, cY))

    
for i in range(len(contours)):
    hull = cv2.convexHull(contours[i])
    cv2.drawContours(diff, [hull], -1, (255, 0, 0), 2)
    
   
    
plt.subplots(figsize=(5, 5))
plt.imshow(diff)
plt.imshow(old)
plt.imshow(new)


test = old.copy()
thresh = cv2.threshold(test, 200, 255, cv2.THRESH_BINARY)[1]

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,10))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

plt.imshow(thresh)

testing = cv2.medianBlur(test, 5)
sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
sharpen = cv2.filter2D(testing, -1, sharpen_kernel)
plt.imshow(test)


thresh = cv2.threshold(sharpen, 160, 255, cv2.THRESH_BINARY_INV)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

plt.imshow(close)
cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]



circles = cv2.HoughCircles(testing, cv2.HOUGH_GRADIENT, 1.2, 100)



gray = cv2.cvtColor(old, cv2.COLOR_BGR2GRAY)
testing = cv2.medianBlur(gray, 7)
circles = cv2.HoughCircles(testing, cv2.HOUGH_GRADIENT, 1.2, 500)

if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        cv2.circle(testing, (i[0], i[1]), i[2], (0, 255, 0), 2)
        
plt.imshow(testing)


thresh = cv2.threshold(testing, 50, 255, cv2.THRESH_BINARY)[1]

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25,25))
opening = cv2.morphologyEx(testing, cv2.MORPH_OPEN, kernel, iterations=3)
plt.imshow(thresh)


import pandas as pd

df = pd.read_csv('/home/pi/Desktop/ditka/tmp.csv', header = None)
df.columns = ['time','x','y']

import altair as alt

alt.Chart(df).mark_circle(size = 10).encode(
    x = 'x',
    y = 'y'
)



