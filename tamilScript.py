import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
from scipy.ndimage import interpolation as inter
import sys
#from google.colab.patches import cv2_imshow
import imutils
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
import pickle
from keras.models import model_from_json
from keras.models import load_model

from pathlib import Path
import os, pickle
import numpy
#from google.colab.patches import cv2_imshow
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from tensorflow.python.client import device_lib

tf.config.experimental.list_physical_devices('GPU')
tf.test.is_gpu_available()

tf.config.list_physical_devices('GPU')
device_lib.list_local_devices()
string = r"upload/"+sys.argv[1]
print(string)
image = cv2.imread(string) # input image location
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
filter1 = cv2.medianBlur(gray,3)

filter2 = cv2.GaussianBlur(filter1,(3,3),0)
dst = cv2.fastNlMeansDenoising(filter2,None,17,7,17)
th1 = cv2.adaptiveThreshold(dst,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,31,5)
#image = cv2.imread("ImagePreProcessingFinal2.jpg")
image=th1
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(th1, (5,5), 0)

ret,thresh1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
print(ret)
print(thresh1)
dilate = cv2.dilate(thresh1, None, iterations=3)
cnts = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[0]

sorted_ctrs = sorted(cnts, key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * image.shape[1] )
import os
orig = image.copy()
i = 0
for cnt in sorted_ctrs:
    # Check the area of contour, if it is very small ignore it
    if(cv2.contourArea(cnt) < 250):
        continue

    # Filtered countours are detected
    x,y,w,h = cv2.boundingRect(cnt)

    # Taking ROI of the cotour
    image2=image
    roi = image[y:y+h, x:x+w]
    #cv2_imshow(roi)
    path = 'Script_Seg_Images' # Seg_Images folder location
    cv2.imwrite(os.path.join(path, str(i)+".jpg"), roi)

    # Mark them on the image if you want
    cv2.rectangle(orig,(x,y),(x+w,y+h),(0,255,0),2)

    # Save your contours or characters
    #cv2.imwrite("Images/roi" + str(i) + ".png", roi)

    i = i + 1

cv2.imwrite("box.jpg",orig)
def prepare(file):
    IMG_SIZE = 50
    img_array = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

#Loading pickle files
file_path_X = open(os.path.join(r"Pickle\X.pickle"), 'rb')#Pickle folder location
file_path_Y = open(os.path.join(r"Pickle\y.pickle"), 'rb')#Pickle folder location
X = pickle.load(file_path_X)
y = pickle.load(file_path_Y)

number_of_classes = max(y) + 1 #Number of classes
X = X/255.0 #Normalising the images
print(X.shape)
y=numpy.asarray(y)

model = tf.keras.models.load_model("CNN_2.model") # model to be loaded in the drive
CATEGORIES = []
files = ['1 - Multipart','2 - Unknown']
DATADIR = r'Seg_Images' #Seg Images location
for directoryfile in os.listdir(DATADIR):
    if(directoryfile in files):
        continue
    CATEGORIES.append(directoryfile)
print(len(CATEGORIES))

import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import numpy as np
image2=th1
orig = image2.copy()
i = 0
I1=Image.open('box.jpg')
for cnt in sorted_ctrs:
    # Check the area of contour, if it is very small ignore it
    if(cv2.contourArea(cnt) < 250):
        continue

    # Filtered countours are detected
    x,y,w,h = cv2.boundingRect(cnt)

    # Taking ROI of the cotour
    roi = image2[y:y+h, x:x+w]
    IMG_SIZE = 50
    img_array = roi
    #cv2_imshow(roi)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    image=new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    prediction = model.predict([image])
    prediction1 = list(prediction[0])
    #print(CATEGORIES[prediction1.index(max(prediction1))]) #print label of max probability
    i=i+1;
    c= CATEGORIES[prediction1.index(max(prediction1))]
    #cv2_imshow(roi)
    #path = '/content/gdrive/MyDrive/Ancient-Tamil-Script-Recognition-master/Seg_Images'
    #cv2.imwrite(os.path.join(path, str(i)+".jpg"), roi)

    # Mark them on the image if you want
    cv2.rectangle(orig,(x,y),(x+w,y+h),(0,255,0),2)



    # Save your contours or characters
    #cv2.imwrite("Images/roi" + str(i) + ".png", roi)

    i = i + 1
    #print(i)

    draw = ImageDraw.Draw(I1)
    # specified font size
    font = ImageFont.truetype(r'CODE2000.TTF', 20) #font type location
    text = c
    # drawing text size
    draw.text((x, y-25), text, font = font, align ="left")
    I1.save("public/Output/final.png")
