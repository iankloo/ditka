import cv2

old = cv2.imread('~/Desk')
new = cv2.imread('/home/pi/Desktop/saved_img2.jpg')

diff = cv2.absdiff(old, old)
print(diff.mean())

