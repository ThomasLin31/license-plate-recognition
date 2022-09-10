# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 05:13:11 2020

@author: k1252
"""

import cv2

def allnumresize(endcount = 58):
    size = (28,28)
    imagelocation = "newimage/nums/"
    outputimagelocation =  "newimage/numsfortrain/"
    count= 0
    endcount = endcount
    
    def resize(filename= ""):
        image = cv2.imread(imagelocation + filename + "%d"%count + ".png" )
        
        image = cv2.resize(image,size)
        image = cv2.bitwise_not(image)
        cv2.imwrite(outputimagelocation + filename + "%d"%count + ".png",image)    
        
    while True:
        if count == endcount:
            break
        resize()
        count+=1
    print ("轉換完畢")
allnumresize(endcount = 58)    
