import cv2
import matplotlib.pyplot as plt
import numpy as np

old = cv2.imread('shot_output/19_shot.jpg')
new = cv2.imread('shot_output/18_shot.jpg')

diff = cv2.absdiff(old, new)
print(diff.mean())









