# 訓練模型用，會生成newModel.h5

import tensorflow as tf
import numpy as np
import PIL
import csv

def numtrain(countend=57):    
    count = 0
    allnum = ""
    
    
    imagelocation = "newimage/numsfortrain/"
    traincount= 0
    trainendcount = countend
    imagetrainarray = []
    
    
    testcount = 0
    testendcount = countend
    imagetestarray = []
    
    
    with open('trainVal.csv', newline='') as csvfile:
    
      # 讀取 CSV 檔案內容
      rows = csv.reader(csvfile)
    
      # 以迴圈輸出每一列
      for row in rows:
        if count >=1 and count%2 == 0:
            allnum += row[2]
        count +=1   
    
    traindata = allnum[:countend]
    mytrainanswerlist = []
    for i in traindata:
        for j in i:
            if j =="A":
                mytrainanswerlist.append(11)
            elif j =="B":
                mytrainanswerlist.append(12)
            elif j =="C":
                mytrainanswerlist.append(13)
            elif j =="D":
                mytrainanswerlist.append(14)
            elif j =="E":
                mytrainanswerlist.append(15)
            elif j =="F":
                mytrainanswerlist.append(16)
            elif j =="G":
                mytrainanswerlist.append(17)
            elif j =="H":
                mytrainanswerlist.append(18)
            elif j =="I":
                mytrainanswerlist.append(19)
            elif j =="J":
                mytrainanswerlist.append(20)
            elif j =="K":
                mytrainanswerlist.append(21)
            elif j =="L":
                mytrainanswerlist.append(22)
            elif j =="M":
                mytrainanswerlist.append(23)
            elif j =="N":
                mytrainanswerlist.append(24)
            elif j =="O":
                mytrainanswerlist.append(25)
            elif j =="P":
                mytrainanswerlist.append(26)
            elif j =="Q":
                mytrainanswerlist.append(27)
            elif j =="R":
                mytrainanswerlist.append(28)
            elif j =="S":
                mytrainanswerlist.append(29)
            elif j =="T":
                mytrainanswerlist.append(30)
            elif j =="U":
                mytrainanswerlist.append(31)
            elif j =="V":
                mytrainanswerlist.append(32)            
            elif j =="W":
                mytrainanswerlist.append(33)
            elif j =="X":
                mytrainanswerlist.append(34)
            elif j =="Y":
                mytrainanswerlist.append(35)
            elif j =="Z":
                mytrainanswerlist.append(10)        
            elif j == "0":
                mytrainanswerlist.append(0)
            elif j == "1":
                mytrainanswerlist.append(1)
            elif j == "2":
                mytrainanswerlist.append(2)
            elif j == "3":
                mytrainanswerlist.append(3)
            elif j == "4":
                mytrainanswerlist.append(4)
            elif j == "5":
                mytrainanswerlist.append(5)
            elif j == "6":
                mytrainanswerlist.append(6)
            elif j == "7":
                mytrainanswerlist.append(7)
            elif j == "8":
                mytrainanswerlist.append(8)
            elif j == "9":
                mytrainanswerlist.append(9)
    
    
    mytrainanswerlist=np.array(mytrainanswerlist)
    
    testdata = allnum[:countend]
    mytestanswerlist =  []
    for i in testdata:
        for j in i:
    
            if j =="A":
                mytestanswerlist.append(11)
            elif j =="B":
                mytestanswerlist.append(12)
            elif j =="C":
                mytestanswerlist.append(13)
            elif j =="D":
                mytestanswerlist.append(14)
            elif j =="E":
                mytestanswerlist.append(15)
            elif j =="F":
                mytestanswerlist.append(16)
            elif j =="G":
                mytestanswerlist.append(17)
            elif j =="H":
                mytestanswerlist.append(18)
            elif j =="I":
                mytestanswerlist.append(19)
            elif j =="J":
                mytestanswerlist.append(20)
            elif j =="K":
                mytestanswerlist.append(21)
            elif j =="L":
                mytestanswerlist.append(22)
            elif j =="M":
                mytestanswerlist.append(23)
            elif j =="N":
                mytestanswerlist.append(24)
            elif j =="O":
                mytestanswerlist.append(25)
            elif j =="P":
                mytestanswerlist.append(26)
            elif j =="Q":
                mytestanswerlist.append(27)
            elif j =="R":
                mytestanswerlist.append(28)
            elif j =="S":
                mytestanswerlist.append(29)
            elif j =="T":
                mytestanswerlist.append(30)
            elif j =="U":
                mytestanswerlist.append(31)
            elif j =="V":
                mytestanswerlist.append(32)            
            elif j =="W":
                mytestanswerlist.append(33)
            elif j =="X":
                mytestanswerlist.append(34)
            elif j =="Y":
                mytestanswerlist.append(35)
            elif j =="Z":
                mytestanswerlist.append(10)
            
            elif j == "0":
                mytestanswerlist.append(0)
            elif j == "1":
                mytestanswerlist.append(1)
            elif j == "2":
                mytestanswerlist.append(2)
            elif j == "3":
                mytestanswerlist.append(3)
            elif j == "4":
                mytestanswerlist.append(4)
            elif j == "5":
                mytestanswerlist.append(5)
            elif j == "6":
                mytestanswerlist.append(6)
            elif j == "7":
                mytestanswerlist.append(7)
            elif j == "8":
                mytestanswerlist.append(8)
            elif j == "9":
                mytestanswerlist.append(9)
    
    mytestanswerlist = np.array(mytestanswerlist)
    print (type(mytestanswerlist[0]))
    
    #train
    
    while True:
        if traincount == trainendcount:  
            break
        trainimage = PIL.Image.open(imagelocation + "%d"%traincount +".png").convert("L")
        imagetrainarray.append(np.asarray(trainimage))    
        traincount+=1
    
    imagetrainarray = np.array(imagetrainarray)
    train = imagetrainarray.reshape(len(imagetrainarray), 28, 28, 1)
    
    #test
    
    while True:
        if testcount == testendcount:  
            break
        testimage = PIL.Image.open(imagelocation + "%d"%testcount +".png").convert("L")
        imagetestarray.append(np.asarray(testimage)) 
        testcount+=1
    
    imagetestarray = np.array(imagetestarray)    
    test = imagetestarray.reshape(len(imagetestarray), 28, 28, 1)
      
    input_shape = (28, 28, 1)
    print(type(test),type(test[0]))
        
    
    
    # 轉成浮點數(為了正規化)
    mytrainanswerlist = mytrainanswerlist.astype('float32')
    mytestanswerlist = mytestanswerlist.astype('float32')
    
    train = train.astype('float32')
    test = test.astype('float32')
    
    # 將灰階(2**8-1=255)的圖片正規化
    train = train / 255
    test = test /255
    
    
    print('x_train shape:', train.shape)
    print('Number of images in x_train:', train.shape[0])
    print('Number of images in x_test:', test.shape[0])
    
    # 導入為了訓練需要的 model & layer 
    from keras.models import Sequential
    from keras.layers import Dense, Conv2D, Dropout, Flatten, MaxPooling2D
    
    # 創建序列模型，並加上layers
    model = Sequential()
    model.add(Conv2D(28, kernel_size=(3,3), input_shape=input_shape, activation='relu'))
    
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten()) 
    model.add(Dense(128, activation=tf.nn.relu))
    model.add(Dropout(0.2))
    model.add(Dense(36,activation=tf.nn.softmax))
    
    model.compile(optimizer='adam', 
                  loss='sparse_categorical_crossentropy', 
                  metrics=['accuracy'])
    
    # 這裡調整epochs
    model.fit(x=train,y=mytrainanswerlist, epochs=40,verbose=0)
    
    model.evaluate(test, mytestanswerlist)
    
    model.save('newModel.h5')  # 儲存model
    del model 
numtrain(countend=57)