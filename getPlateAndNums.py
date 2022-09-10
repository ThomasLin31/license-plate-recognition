# -*- coding: utf-8 -*-
"""
Created on Wed Mar 8 08:12:16 2020

@author: k1252
"""
import cv2 # OpenCV:用來做圖片處理
import imutils # 把圖片等比例縮放


           


def getPlateAndNums(countend=10):
    
    #loop count
    count = 1
    count3 = 0
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
                if largest != []:
                    if len(largest[0]) >= 4 :
                        print ("第幾張",count,"參數",largest[0][3]) # 印出最佳的參數
                
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
        
    print ("數字:",count3,"個") # 共多少數字
    
getPlateAndNums(countend=10)