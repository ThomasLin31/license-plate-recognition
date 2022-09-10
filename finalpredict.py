# -*- coding: utf-8 -*-
import cv2 # OpenCV:用來做圖片處理
import imutils # 把圖片等比例縮放
import numpy as np
import PIL
import tensorflow as tf
from tensorflow import keras


def getPlateAndNums(countend):
    
    global count,count3
    # 迴圈
    while True:
        
        if count == countend: #中止點
            break
         
        oriimage = cv2.imread("predict/test/"+"%d.jpg"%count) # 讀取原始圖片並轉成灰階
        oriimage = imutils.resize(oriimage, width = 500) # 把圖片等比例弄成寬度500
        h,w,d =oriimage.shape # 取圖片的高度、寬度、顏色深度
        
        
        image = oriimage
        image = cv2.bilateralFilter(image, 10,20,20) # 雙邊濾波，後面3個參數為d(每個像素周圍的直徑), sigmaColor(這個值越大，代表周圍越不相似的值會視為相同), sigmaSpace(這個值越大，代表越遠且顏色相近的像素會彼此影響)
        image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) # 轉灰階
    
        reimage = imutils.resize(image, width = 500) # 把圖片等比例弄成寬度500
        
        count4 = 0 # 特徵值的變數
        allnums = []
        while True:
            
            nocontour = False # 沒有輪廓時的變數
            nocontour2 = False # 沒有輪廓時的變數
    
            if count4 ==250: # 特徵值的中止點
                
                largest = sorted(allnums, key=lambda tup: tup[2])
                largest = sorted(largest, key=lambda tup: tup[0] ,reverse=True)[:1]
                #if largest != []:
                    #if len(largest[0]) >= 4 :
                        #print ("第幾張",count,"參數",largest[0][3]) # 印出最佳的參數
                
                if largest == []:
                    nocontour2 = True
                    break
                else:
                    a, image = cv2.threshold(reimage,largest[0][3],255,cv2.THRESH_BINARY)
       
            else:
                a, image = cv2.threshold(reimage,250-count4,255,cv2.THRESH_BINARY)
    
            contours, hierarchy = cv2.findContours(image,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #找出輪廓(形成封閉區域)
            contours = sorted(contours, key = cv2.contourArea, reverse = True)[:1] # 做逆方向排序，並取出最大的(因為最有可能是車牌)
            
            
            if contours !=[]:
                length = cv2.arcLength(contours[0], True)  # 輪廓的周長(True代表要封閉的)
                approx = cv2.approxPolyDP(contours[0], 0.051*length, True) # 求逼近的X邊形
                
            else:
                nocontour = True # 找不到車牌輪廓時
            
            
            ###   取得車牌   ###     
                
            if len(approx) != 4 or nocontour == True: # 如果車牌輪廓不是四邊形或找不到輪廓
                count4+=1 # 特徵值+1
                continue # 找下一個特徵值
        
            
            newapprox = []
            
            for i in approx:
                newapprox.append((i[0][0],i[0][1])) # 每個車牌輪廓點的X和Y          
            xsortapprox = sorted(newapprox, key=lambda tup: tup[0]) # 把每個車牌輪廓點做排序(依照x從小到大)
            ysortapprox = sorted(newapprox, key=lambda tup: tup[1]) # 把每個車牌輪廓點做排序(依照y從小到大)
          
            
            
            
            # 分割的點 ##
            #圖片左上角為(0,0)，往右x增加，往下y增加        
            lx = xsortapprox[0][0] # 車牌輪廓最左邊(最小的X)
            rx = xsortapprox[3][0] # 車牌輪廓最右邊(最大的X)
            uy = ysortapprox[0][1] # 車牌輪廓最上面(最小的y)
            dy = ysortapprox[3][1] # 車牌輪廓最下面(最大的y)
            cropimage = image[uy:dy,lx:rx] # 分割出車牌的圖片
            cv2.imwrite("newimage/crop/%d.png" %count ,cropimage)# 儲存圖片
            cv2.imwrite("newimage/crop2/%d.png" %count ,cropimage)# 儲存圖片
                
                
            ###   分割車牌數字   ###
            
            # 讀取圖片
            image = cv2.imread("newimage/crop/%d.png" %count) # 用來分割數字
            image2 = cv2.imread("newimage/crop2/%d.png" %count) # 用來畫圖
            
            image = cv2.bitwise_not(image) # 黑轉白白轉黑
            gimage = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #轉灰階
            h,w = gimage.shape # 取圖片的高和寬
            
            contours, hierarchy = cv2.findContours(gimage,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #找出輪廓(形成封閉區域)
    
            contours = sorted(contours, key = cv2.contourArea, reverse = True)
            
            
            allxywidthheightrec = []
    
    
            # 整理輪廓(排序)
            for i in contours:
                
                
                length = cv2.arcLength(i, True)  # 輪廓的周長(True代表要封閉的)
                approx = cv2.approxPolyDP(i, 0.03*length, True) # 求逼近的X邊形
                newapprox2 = []
                for j in approx:
                    newapprox2.append((j[0][0],j[0][1]))
                xsortapprox = sorted(newapprox2, key=lambda tup: (tup[0]))
                ysortapprox = sorted(newapprox2, key=lambda tup: (tup[1]))                    
                allxywidthheightrec.append(((xsortapprox[0][0],xsortapprox[-1][0]),(ysortapprox[0][1],ysortapprox[-1][1]),xsortapprox[-1][0]-xsortapprox[0][0],ysortapprox[-1][1]-ysortapprox[0][1],((xsortapprox[0][0],ysortapprox[0][1]),(xsortapprox[-1][0],ysortapprox[-1][1]))))
    
            allxywidthheightrec = sorted(allxywidthheightrec)
    
    
            
            
            nums = 0 # 總共找出多少數字
            averageh = 0
            averagew = 0
            average2 = []
            betested = []
            
            # 限制輪廓的寬高
            for i in range(len(allxywidthheightrec)):
    
                if   allxywidthheightrec[i][2]< int(w/6)  and 1 < allxywidthheightrec[i][0][0] and w-1 > allxywidthheightrec[i][0][1]:
    
                    if int(h/4) < allxywidthheightrec[i][3]:
     
                        nums +=1
                        averageh += allxywidthheightrec[i][3]
                        averagew += allxywidthheightrec[i][2]
                        average2.append((allxywidthheightrec[i][3],allxywidthheightrec[i][2]))
                        betested.append(allxywidthheightrec[i])
            
            # 如果符合的輪廓很多，則將極值(比平均高度過高或過低)排除
            if nums != 0:
                removelist =[]
                averageh = 0
                for i in range(len(betested)):
                    averageh += betested[i][3]
                averageh = averageh/nums
                for i in range(len(betested)):
                    if betested[i][3] < 3*averageh/4 or betested[i][3] > 4*averageh/3:
                        removelist.append(i)
                        nums -=1
                if removelist != []:  
                     
    
                    for i in reversed(removelist):
                        del average2[i]
                        del betested[i] 
                        averageh -= allxywidthheightrec[i][3]
                        averagew -= allxywidthheightrec[i][2]
                        
                averageh = averageh/nums
                averagew = averagew/nums
                allnums.append((nums,averageh,averagew,250-count4))
                
    
            if count4 ==250: # 特徵值中止
                break
                   
            count4+=1
            
            
            
    
        if nocontour2 == True: # 如果試了250個特徵數值都找不到輪廓，則直接換下一張圖片
            count += 1 # 換下一張圖片       
            continue   
    
    
        for i in range(len(betested)):
    
            cv2.rectangle(image2,betested[i][4][0],betested[i][4][1], (255,0,0),2)
            
            cropimage = image[betested[i][4][0][1]-1:betested[i][4][1][1]+1,betested[i][4][0][0]:betested[i][4][1][0]]
            cropimage = cv2.resize(cropimage,(28,28))
            cropimage = cv2.bitwise_not(cropimage)
            cv2.imwrite("newimage/nums/%d.png" %count3,cropimage)
            count3+=1
                    
                    
      
        cv2.imwrite("newimage/drawrec/%d.png" %count ,image2)
        count += 1

        


def allnumresize(resizeendcount):
    global resizecount
    size = (28,28)
    imagelocation = "newimage/nums/"
    outputimagelocation =  "newimage/numsfortrain/"
    endcount = count3
    
    def resize(filename= ""):
        image = cv2.imread(imagelocation + filename + "%d"%resizecount + ".png" )
        
        image = cv2.resize(image,size)
        image = cv2.bitwise_not(image)
        cv2.imwrite(outputimagelocation + filename + "%d"%resizecount + ".png",image)    
        
    while True:
        if resizecount == endcount:
            break
        resize()
        resizecount+=1
        
def predict(predictendcount):
    global predictcount,result
    model1 = tf.keras.models.load_model("newModel.h5")
    
    while True:
        if predictcount == predictendcount:
            break
        image = PIL.Image.open("newimage/nums/%d.png" %predictcount).convert('L') # 圖片轉成灰階 
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
          

        result +=str(finalpred)
        predictcount +=1


resizecount = 0
predictcount = 0       
count3 = 0 
def main(imgcount):
    global count3,resizecount,predictcount,count,countend,result

    count = imgcount+1

    result=""
    print ("第%d張:"%count)
    print (" 預測數字:",end="")
    countend = count+1
    getPlateAndNums(countend)
    resizeendcount = count3+1
    allnumresize(resizeendcount)
    predictendcount = count3
   
    predict(predictendcount)
    print(result)
    
    
import tkinter as tk
from PIL import Image, ImageTk, ImageFilter

class Panel(object):


    def __init__(self):
        
        self.root = tk.Tk()
        self.root.title("簡易車牌辨識")
        self.img_ref = []
            
        # 辨識按鈕
        self.recognize = tk.Button(self.root, text='辨識',width=8,height=3,font=("微軟正黑體", 10), command=lambda:  self.Predict(1) )
        self.recognize.grid(row=0, column=0, padx=5, pady=5)
        
        # 下一張
        self.next = tk.Button(self.root, text='下一個',width=8,height=3,font=("微軟正黑體", 10), command= self.Next )
        self.next.grid(row=0, column=2, padx=5, pady=5)
        self.imgcount = 0
        
        
        # 原圖片
        self.image = tk.Canvas(self.root, width=140, height=150,highlightthickness=0, relief='ridge')
        self.image.create_image(0, 0, anchor="nw", tags="img1")
        self.image.grid(row=1, columnspan=2, padx=5, pady=5)
        
        # 辨識圖片
        self.image2 = tk.Canvas(self.root, width=140, height=150,highlightthickness=0, relief='ridge')
        #self.image2.create_image(0, 0, anchor="nw", tags="img2")
        self.image2.grid(row=2, columnspan=2, padx=5, pady=5)

        # 第一張圖片
        self.Setup()
        
        # 預測結果
        self.result = tk.Text(self.root, height=2, width=10,spacing1=10,spacing3=10,
                                        borderwidth=0,font=("微軟正黑體", 15), highlightthickness=0,
                                        relief='ridge')
        self.result.tag_configure("center", justify='center')
        self.result.grid(row=1, column=2,columnspan=2)

        
        self.root.mainloop()
        
        
    
    def Setup(self):
        self.img1 = Image.open("predict/%d.jpg"%(self.imgcount+1))
        self.ShowImg(0,self.img1)
        
    # 下一張圖片
    def Next(self):
        self.result.delete(1.0, "end") # 清空文字
        self.imgcount +=1
        if self.imgcount ==8:
            self.imgcount = 0
        self.img1 = Image.open("predict/%d.jpg"%(self.imgcount+1))
        self.ShowImg(0,self.img1)
        self.image2.delete("img2")
        
    # 預測    
    def Predict (self,imgcount):
        main(self.imgcount)
        self.result.insert("end", "預測為:\n {}".format(result), 'center') # 顯示結果
        self.img2 = Image.open("newimage/drawrec/%d.png"%(self.imgcount+1))
        self.ShowImg(1,self.img2)
        
        
    # 顯示結果圖片    
    def ShowImg(self,canvasid, image):
        
        if canvasid ==0:
            self.image.delete("img1")
    
            size = (150, 150)
            resized = image.resize(size, Image.ANTIALIAS)
            
            self.shownimg = ImageTk.PhotoImage(resized)
            self.root.shownimg = self.shownimg
            self.image.create_image(0, 0, image=self.shownimg, anchor="nw", tags="1img")
            self.img_ref.append(self.shownimg)
        else:
            size = (120, 50)
            resized = image.resize(size, Image.ANTIALIAS)
            self.shownimg = ImageTk.PhotoImage(resized)
            self.root.shownimg = self.shownimg
            #self.image2.delete("img2")
            self.image2.create_image(0, 0, image=self.shownimg, anchor="nw", tags="img2")
            self.img_ref.append(self.shownimg)
            

            
if __name__ == '__main__':       
    Panel()
    
    