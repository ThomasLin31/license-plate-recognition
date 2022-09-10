# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 03:38:48 2020

@author: k1252
"""
import numpy as np
import PIL
import keras

def predict(countend=58):
    model1 = keras.models.load_model ("newModel.h5")
    
    count = 0
    while True:
        if count == countend:
            break
        image = PIL.Image.open("newimage/nums/%d.png" %count).convert('L') # 圖片轉成灰階 
        image = image.resize((28,28))
        
        pixel = list(image.getdata())
        Npixel = [(255 - x) * 1.0 / 255.0 for x in pixel]
        
        ANpixel = np.array(Npixel)
        ANpixel = ANpixel.reshape(28,28)
        pred = model1.predict(ANpixel.reshape(1, 28, 28, 1))#預測
        
        if pred.argmax() == 0:
            finalpred = "0"   
        elif pred.argmax() == 1:
            finalpred = "1"   
        elif pred.argmax() == 2:
            finalpred = "2"
        elif pred.argmax() == 3:
            finalpred = "3"
        elif pred.argmax() == 4:
            finalpred = "4"
        elif pred.argmax() == 5:
            finalpred = "5"
        elif pred.argmax() == 6:
            finalpred = "6"
        elif pred.argmax() == 7:
            finalpred = "7"
        elif pred.argmax() == 8:
            finalpred = "8"
        elif pred.argmax() == 9:
            finalpred = "9"
        elif pred.argmax() == 10:
            finalpred = "Z"
        elif pred.argmax() == 11:
            finalpred = "A"
        elif pred.argmax() == 12:
            finalpred = "B"
        elif pred.argmax() == 13:
            finalpred = "C"
        elif pred.argmax() == 14:
            finalpred = "D"
        elif pred.argmax() == 15:
            finalpred = "E"
        elif pred.argmax() == 16:
            finalpred = "F"
        elif pred.argmax() == 17:
            finalpred = "G"
        elif pred.argmax() == 18:
            finalpred = "H"
        elif pred.argmax() == 19:
            finalpred = "I"
        elif pred.argmax() == 20:
            finalpred = "J"
        elif pred.argmax() == 21:
            finalpred = "K"
        elif pred.argmax() == 22:
            finalpred = "L"
        elif pred.argmax() == 23:
            finalpred = "M"
        elif pred.argmax() == 24:
            finalpred = "N"
        elif pred.argmax() == 25:
            finalpred = "O"        
        elif pred.argmax() == 26:
            finalpred = "P"               
        elif pred.argmax() == 27:
            finalpred = "Q"        
        elif pred.argmax() == 28:
            finalpred = "R"        
        elif pred.argmax() == 29:
            finalpred = "S"        
        elif pred.argmax() == 30:
            finalpred = "T"        
        elif pred.argmax() == 31:
            finalpred = "U"        
        elif pred.argmax() == 32:
            finalpred = "V"        
        elif pred.argmax() == 33:
            finalpred = "W"        
        elif pred.argmax() == 34:
            finalpred = "X"        
        elif pred.argmax() == 35:
            finalpred = "Y"        
     
                    
        #print ("預測的數字:")
        print(finalpred,end="")#印出陣列中最大的數值
        count +=1
        #time.sleep(0.5)
        
predict(countend=58)