#original source https://github.com/kevinam99/capturing-images-from-webcam-using-opencv-python/blob/master/webcam-capture-v1.01.py
import cv2 


key = cv2. waitKey(1)
webcam = cv2.VideoCapture(0)
check, frame = webcam.read()

#convert to grayscale
img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#write it out
#cv2.imshow("Capturing", img)
cv2.imwrite(filename='saved_img3.jpg', img=img)

#shut down
webcam.release()
cv2.destroyAllWindows()
        
