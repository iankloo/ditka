#original source https://github.com/kevinam99/capturing-images-from-webcam-using-opencv-python/blob/master/webcam-capture-v1.01.py
import cv2
import os
import csv
import datetime
from tkinter import *
from datetime import datetime


# Creating the tkinter window
root = Tk()
root.title('Camera is monitoring target...')
root.geometry("400x100")
  
# Button for closing
exit_button = Button(root, text="Stop Camera", command=root.destroy)
exit_button.pack(pady=20)
  
root.mainloop()


#create empty CSV
# header = ['timestamp', 'x', 'y']
# with open('tmp.csv', 'w') as f: 
#     csvwriter = csv.writer(f)
#     csvwriter.writerow(header)
#     f.close()

#setup web cam
webcam = cv2.VideoCapture(0)

#read first image
check, frame = webcam.read()
frame = cv2.flip(frame, -1)
orig_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#make folder for debug images
write_file = '/media/pi/USB_DRIVE/shot_data/shot_output_' + str(datetime.now()) + '/'
#files = os.listdir(write_file)


#write first image to file for debug

# files = os.listdir(write_file)
# if len(files) > 0:
#     orig_img = cv2.imread(write_file+files[-1])
#     orig_img = cv2.cvtColor(orig_img, cv2.COLOR_BGR2GRAY)
#     file_counter = int(files[-1].split('_')[0])
# else:
#save initial image
orig_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
cv2.imwrite(filename=write_file+'0_shot.jpg', img=orig_img)
file_counter = 1

    
while True:
    try:
        #get new image
        check, frame = webcam.read()
        frame = cv2.flip(frame, -1)
        
        #compare to the first image
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(img, orig_img)
        
        #if not the same, figure out where new shot is
        #try to up the sensitivity
        if diff.mean() > 3:
            #just output images now to see what we get
            cv2.imwrite(filename=write_file+str(file_counter)+'_shot.jpg', img=img)
            orig_img = img
            file_counter += 1

            
            
#             #print('go')
#             log_time = datetime.datetime.now()
#             #diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
#             diff = cv2.blur(diff, (10, 10)) # blur the image
            
#             ret, thresh = cv2.threshold(diff,50,255,0)
#             contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
#             center_coords = []
#             for c in contours:
#                 try:
#                     M = cv2.moments(c)
#                     cX = int(M["m10"] / M["m00"])
#                     cY = int(M["m01"] / M["m00"])

#                     center_coords.append((log_time, cX, cY))
#                 except:
#                     pass
#             if len(center_coords) > 0:
#                 #print(center_coords)
#                 with open('tmp.csv', 'a') as f:
#                     writer = csv.writer(f)
#                     writer.writerows(center_coords)

                #overwrite original image with the new one for future comparisons
                #orig_img = img
            
    except(KeyboardInterrupt):
        webcam.release()
        cv2.destroyAllWindows()
        break

