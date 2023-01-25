import cv2
import imutils
import time
import os 

cv2.namedWindow('preview')
vid = cv2.VideoCapture(0)

if vid.isOpened():
    ret, frame = vid.read()
else:
    ret = False

clicked = False
def onMouse(event, x, y, flags, param):
    global clicked
    if event == cv2.EVENT_LBUTTONUP:
        clicked = True

cv2.setMouseCallback('preview', onMouse)
    
while(not clicked):
    flipped = cv2.flip(frame, -1)
    cv2.imshow('preview', flipped)
    
    ret, frame = vid.read()
    frame = imutils.resize(frame, width=480)

    #draw crosshairs
    height, width, channels = frame.shape
    #cv2.circle(img=frame, center = (int(width/2),int(height/2)), color=(0, 0, 255), radius = 10, thickness=-1)
    cv2.line(frame, (int(width/2), int(height/2)+15), (int(width/2), int(height/2)-15), color=(0, 0, 255), thickness=2)
    cv2.line(frame, (int(width/2)-15, int(height/2)), (int(width/2)+15, int(height/2)), color=(0, 0, 255), thickness=2)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    
    
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows() 

os.system('python /home/pi/Desktop/ditka/monitor_target.py')