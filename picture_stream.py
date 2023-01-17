#original source https://github.com/kevinam99/capturing-images-from-webcam-using-opencv-python/blob/master/webcam-capture-v1.01.py
import cv2
import os
import time

#setup web cam
webcam = cv2.VideoCapture(0)
check, frame = webcam.read()

#check if there are already images there, make the last one the one for comparison
files = os.listdir('/home/pi/Desktop/shot_output/')
if len(files) > 0:
    orig_img = cv2.imread('/home/pi/Desktop/shot_output/'+files[-1])
    orig_img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2GRAY)
    file_counter = int(files[-1].split('_')[0])
else:
    #save initial image
    orig_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(filename='/home/pi/Desktop/shot_output/0_shot.jpg', img=orig_img)
    file_counter = 1
    
while True:
    try:
        #get new image
        check, frame = webcam.read()
        
        #compare to the first image
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(img, orig_img).mean()
        
        #if not same, save new image and overwrite original for comparisons
        if diff > 20:
            cv2.imwrite(filename='/home/pi/Desktop/shot_output/'+str(file_counter)+'_shot.jpg', img=img)
            orig_img = img
            file_counter += 1
            
    except(KeyboardInterrupt):
        webcam.release()
        cv2.destroyAllWindows()
        break

