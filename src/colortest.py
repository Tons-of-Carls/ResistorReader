    # -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 00:35:26 2019

@author: lolly
"""

CONST_BLACK = 0 
CONST_BROWN = 1 
CONST_RED = 2 
CONST_ORANGE = 3 
CONST_YELLOW = 4 
CONST_GREEN = 5 
CONST_BLUE = 6 
CONST_VIOLET = 7 
CONST_GRAY = 8 
CONST_WHITE = 9 
CONST_SILVER = 10 
CONST_GOLD = 11

DEBUG = True
 
import numpy as np
import matplotlib.pyplot as plt
import scipy.misc as misc
from Calculation import Calculator

from identifycolor import colorIdentifier

def crop (name):
    
    def betwnValues(val, min, max):
        return (val > min) * (val < max)
    
    img = plt.imread(name)
    plt.imshow(img)
    plt.show()

    img = img[int(img.shape[0]*.15):-int(img.shape[0]*.15)]

    if DEBUG:
        plt.imshow(img)
        plt.show()


    batchWidth = 8 
 
    (h, w) = img.shape[:2] 
    w2 = int(np.ceil(w / float(batchWidth))) 
 
    mods = w % batchWidth 
    if mods == 0: 
        pw = (0, 0) 
    else: 
        pw = (0, batchWidth - mods) 
 
    img = np.stack((np.pad(img[:,:,0], ((0,h), pw), 'symmetric'),np.pad(img[:,:,1], ((0,h), pw), 'symmetric'),np.pad(img[:,:,2], ((0,h), pw), 'symmetric')), axis=-1) 
 
 
    averaged_vals = np.zeros([1,w2,3]) 
    for i in range(w2): 
        r = np.mean(img[:, i * batchWidth:(i + 1) * batchWidth, 0]) 
        b = np.mean(img[:, i * batchWidth:(i + 1) * batchWidth, 1]) 
        g = np.mean(img[:, i * batchWidth:(i + 1) * batchWidth, 2]) 
 
        averaged_vals[0][i][0] = r 
        averaged_vals[0][i][1] = b 
        averaged_vals[0][i][2] = g 
        
    averaged_vals = np.stack((averaged_vals[0],averaged_vals[0],averaged_vals[0],averaged_vals[0],averaged_vals[0],averaged_vals[0]), axis=0)
    if DEBUG:
        plt.imshow(averaged_vals.astype(int))
        plt.show()

    misc.toimage(averaged_vals, cmin=0.0, cmax=255.0).save("img.jpg")
    
    identifier = colorIdentifier("./img.jpg")
    #print("hi")
    thresh = 30
    for i in range(w2):
        if(averaged_vals[0][i][0] < (identifier.getDominant()[0]+thresh) and averaged_vals[0][i][0] > (identifier.getDominant()[0]-thresh)) :
            if(averaged_vals[0][i][1] < (identifier.getDominant()[1]+thresh) and averaged_vals[0][i][1] > (identifier.getDominant()[1]-thresh)) :
                if(averaged_vals[0][i][2] < (identifier.getDominant()[2]+thresh) and averaged_vals[0][i][2] > (identifier.getDominant()[2]-thresh)) :
                    averaged_vals = averaged_vals[:,i:]
                    break
    
    for i in range(averaged_vals.shape[1]-1, -1,-1):
        if(averaged_vals[0][i][0] < (identifier.getDominant()[0]+thresh) and averaged_vals[0][i][0] > (identifier.getDominant()[0]-thresh)) :
            if(averaged_vals[0][i][1] < (identifier.getDominant()[1]+thresh) and averaged_vals[0][i][1] > (identifier.getDominant()[1]-thresh)) :
                if(averaged_vals[0][i][2] < (identifier.getDominant()[2]+thresh) and averaged_vals[0][i][2] > (identifier.getDominant()[2]-thresh)) :
                    averaged_vals = averaged_vals[:,:i]
                    break
    
    #green_filter = betwnValues(averaged_vals[:,:,0], 130, 170) * betwnValues(averaged_vals[:,:,1], 130, 170) * betwnValues(averaged_vals[:,:,2], 130, 170)
    if DEBUG:
        plt.imshow(averaged_vals.astype(int))
        plt.show()
    
    #plt.imshow(green_filter)
    #plt.show()
    
    return averaged_vals 

def showColor (array, color): 
      
     def black(): #black looks grayish 
         black_filter = (array[:,:,0] < 60) * (array[:,:,1] < 60) *  (array[:,:,2] < 60)
         plt.imshow(black_filter) 
         plt.show() 
         print(color) 
         return black_filter
     def brown(): 
         brown_filter = ((array[:,:,0]*1.0/array[:,:,1])<2.2) * (array[:,:,0] > 50)* (array[:,:,0] < 180) * (array[:,:,1] > 20) * (array[:,:,1] < 90) * (array[:,:,2] > 10) * (array[:,:,2] < 90)
         plt.imshow(brown_filter)  
         plt.show() 
         print(color) 
         return brown_filter
     def red(): 
         red_filter = ((array[:,:,0]*1.0/array[:,:,1])>2.2) * (array[:,:,0] > 100) * (array[:,:,1] > 30) * (array[:,:,1] < 80) * (array[:,:,2] > 20) * (array[:,:,2] < 90)
         plt.imshow(red_filter) 
         plt.show() 
         print(color)
         return red_filter
     def orange(): 
         orange_filter = ((array[:,:,1]*1.0/array[:,:,2])>1.4) * (array[:,:,0] > 160) * (array[:,:,1] > 60) * (array[:,:,1] < 130) * (array[:,:,2] > 15) * (array[:,:,2] < 100) 
         plt.imshow(orange_filter) 
         plt.show() 
         print(color)
         return orange_filter
     def yellow(): 
         yellow_filter = (array[:,:,0] > 160) * (array[:,:,1] > 140) * (array[:,:,1] < 200) * (array[:,:,2] > 10) * (array[:,:,2] < 80) 
         plt.imshow(yellow_filter) 
         plt.show() 
         print(color) 
         return yellow_filter
     def green(): 
         green_filter = (array[:,:,0] > 50) * (array[:,:,0] < 125) * (array[:,:,1] > 60) * (array[:,:,2] < 90) * (array[:,:,2] > 30) 
         plt.imshow(green_filter) 
         plt.show() 
         print(color) 
         return green_filter
     def blue(): 
         blue_filter = (array[:,:,0] > 10) * (array[:,:,0] < 50) * (array[:,:,1] > 80) * (array[:,:,1] < 120) * (array[:,:,2] > 150) 
         plt.imshow(blue_filter) 
         plt.show() 
         print(color) 
         return blue_filter
     def violet(): 
         violet_filter = (array[:,:,0] > 100) * (array[:,:,0]  < 190) * (array[:,:,1] > 70) * (array[:,:,1] < 140) * (array[:,:,2] > 120) * (array[:,:,2] < 180)
         plt.imshow(violet_filter) 
         plt.show() 
         print(color) 
         return violet_filter
     def gray(): 
         gray_filter = (array[:,:,0] > 130) * (array[:,:,0] < 150) * (array[:,:,1] > 120) * (array[:,:,1] < 140) * (array[:,:,2] > 100) * (array[:,:,2] < 120)
         if DEBUG:
             plt.imshow(gray_filter)
             plt.show()
             print(color)
         return gray_filter
     def white(): 
         white_filter = (array[:,:,0] > 200) * (array[:,:,1] > 200) * (array[:,:,2] > 200)
         if DEBUG:
             plt.imshow(white_filter)
             plt.show()
             print(color)
         return white_filter
         
     filters = {  0: black, 
                 1: brown, 
                 2: red, 
                 3: orange, 
                 4: yellow, 
                 5: green, 
                 6: blue, 
                 7: violet, 
                 8: gray, 
                 9: white, 
                 #10: silver, 
                 #11: gold, 
             } 
 
     return filters[color] ()
   
# Four-band resistors

ohm_calculator_4 = Calculator(4)
# Four-band resistors  
          #r7, 11, 12, 13, 16, 19, 20, 21, 22, 23, 24, 25, 26, 27
          #r1, 2, 3, 4, 5, 6, 9, 10, 15, 17, 18
for x in range (15,16): 
    pic = "../imgs/r" + str(x) + ".jpg" 
    print("r" + str(x)) 
    array = crop(pic) 
    blackDetected = False
    brownDetected = False
    locations = np.zeros((3,2))
    c = 0
    for y in range (0,10): 
        detection = showColor(array,y)
        pos = np.argwhere(detection)
        if pos.shape[0] > 0 and y != 8:
            if blackDetected and (y == 1 or y == 5):
                continue
            if y==0:
                blackDetected = True
            if brownDetected and y == 5:
                continue
            if y == 1:
                brownDetected = True
            prev = -1
            for p in pos:
                print(p)
                if p[1] - prev > 1:
                    locations[c][0] = p[1]
                    locations[c][1] = y
                    c+=1
                if p[0]!=0:
                    break
                prev = p[1]
    locations = sorted(locations, key=lambda x:x[0])
    print(10**locations[2][1])
    print(ohm_calculator_4.calculate(locations[0][1],locations[1][1],10**locations[2][1], .1), "Ohms")
        
#for x in range (1,10):
#     pic = "../imgs/r" + str(x) + ".jpg" 
#     print("r" + str(x)) 
#     array = crop(pic) 

#     for y in range (0,10):
#         showColor(array,y)


#for x in range (1,10):
#    pic = "..imgs/5Band" + str(x) + ".jpg"
#    print("5Band" + str(x))
#    array = crop(pic)
    
##        showColor(array,y) 
         

