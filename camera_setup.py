import cv2

cv2.namedWindow('preview')
vid = cv2.VideoCapture(0)

if vid.isOpened():
    ret, frame = vid.read()
else:
    ret = False

while(True):

    cv2.imshow('preview', frame)
    ret, frame = vid.read()

    #frame is 640x480 by default, so center is half of that
    #cv2.circle(img=frame, center = (320,240), color=(0, 0, 255), radius = 10, thickness=-1)
    cv2.line(frame, (310, 240), (330, 240), color=(0, 0, 255), thickness=2)
    cv2.line(frame, (320, 230), (320, 250), color=(0, 0, 255), thickness=2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()