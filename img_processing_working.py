import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from skimage.metrics import structural_similarity as compare_ssim

#find the best way to determine if img actually changed
diff_score = []
for i in range(0, 26):
    old = cv2.imread('shot_output/'+str(i)+'_shot.jpg')
    new = cv2.imread('shot_output/'+str(i+1)+'_shot.jpg')
    old = cv2.cvtColor(old, cv2.COLOR_BGR2GRAY)
    new = cv2.cvtColor(new, cv2.COLOR_BGR2GRAY)

    diff_score.append(compare_ssim(old, new))

alpha = 0.5 # Contrast control
beta = 1 # Brightness control
adjusted = cv2.convertScaleAbs(new, alpha=alpha, beta=beta)


def automatic_brightness_and_contrast(image, clip_hist_percent=25):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate grayscale histogram
    hist = cv2.calcHist([gray],[0],None,[256],[0,256])
    hist_size = len(hist)

    # Calculate cumulative distribution from the histogram
    accumulator = []
    accumulator.append(float(hist[0]))
    for index in range(1, hist_size):
        accumulator.append(accumulator[index -1] + float(hist[index]))

    # Locate points to clip
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum/100.0)
    clip_hist_percent /= 2.0

    # Locate left cut
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1

    # Locate right cut
    maximum_gray = hist_size -1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1

    # Calculate alpha and beta values
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha

    '''
    # Calculate new histogram with desired range and show histogram 
    new_hist = cv2.calcHist([gray],[0],None,[256],[minimum_gray,maximum_gray])
    plt.plot(hist)
    plt.plot(new_hist)
    plt.xlim([0,256])
    plt.show()
    '''

    auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return (auto_result, alpha, beta)



adjusted = automatic_brightness_and_contrast(old)

plt.imshow(new)
plt.imshow(adjusted[0])


old, alpha, beta = automatic_brightness_and_contrast(old)
new, alpha, beta = automatic_brightness_and_contrast(new)

diff = cv2.absdiff(old, new)
#print(diff.mean())


diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
diff = cv2.blur(diff, (10, 10)) # blur the image

plt.imshow(diff)


ret, thresh = cv2.threshold(diff,30,255,0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

center_coords = []
for c in contours:
    try:
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        center_coords.append((cX, cY))
    except:
        continue



plot_df = pd.DataFrame(center_coords)
plot_df.columns = ['x','y']

plt.axis([0, 640,  480, 0])
plt.scatter(plot_df['x'],plot_df['y'])
