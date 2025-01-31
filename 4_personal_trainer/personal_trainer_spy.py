import cv2
import numpy as np
import mediapipe as mp
import math

#gerekli kutuphaneler



#yaptigimiz hareketlerin tekrarini sayan bir personal trainer yapalim




def findAngle(img, p1, p2, p3, lmList, draw = True):
    
    #vucutta belirledigimiz 3 noktanin x ve y sini hesapliyoruz.
    x1, y1 = lmList[p1][1:] 
    x2, y2 = lmList[p2][1:] 
    x3, y3 = lmList[p3][1:] 
    
    # açılari hesapliyoruz.
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    if angle < 0: angle += 360
    
    
    #belirledigimiz noktalara yuvarlaklar cizdirip 3 nokta arasinda line atiyoruz ve kac derece aci oldugunu yazdiriyoruz.
    if draw:
        cv2.line(img, (x1, y1), (x2, y2), (0,0,255), 3)
        cv2.line(img, (x3, y3), (x2, y2), (0,0,255), 3)
        
        cv2.circle(img, (x1,y1), 10, (0,255,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 10, (0,255,255), cv2.FILLED)
        cv2.circle(img, (x3,y3), 10, (0,255,255), cv2.FILLED)
        
        cv2.circle(img, (x1,y1), 15, (0,255,255))
        cv2.circle(img, (x2,y2), 15, (0,255,255))
        cv2.circle(img, (x3,y3), 15, (0,255,255))
        
        cv2.putText(img, str(int(angle)), (x2 - 40, y2 + 40), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,255), 2)
    return angle

cap = cv2.VideoCapture("video2.mp4")

mpPose = mp.solutions.pose    #pose modulunu cagiriyoruz
pose = mpPose.Pose()    #mppose u kullanarak pose fonksiyonunu cagiriyoruz
mpDraw = mp.solutions.drawing_utils      #gorsellestirmeyi yapiyoruz

dir = 0
count = 0
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)     #rgb cevirimini yapiyoruz
    
    results = pose.process(imgRGB)
    
    lmList = []
    if results.pose_landmarks:      #bir cikti aldigi surece gelmesi icin if blogu ekliyoruz
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
    
        #insan ustunde olan noktaciklari idsine gore aliyoruz
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, _ = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            lmList.append([id, cx, cy])      #her listenin kordinatlarini lmList e ekliyoruz
    # print(lmList)
    
    #simdi aci bulucaz ve aciya gore yaptiklari hareketleri saydirma islemini yapicaz.
    if len(lmList) != 0:
        
        #sinav icin vucuttaki gerekli yerlerin id sini giriyoruz.
        
        # angle = findAngle(img, 11, 13, 15, lmList)
        
        #simdi ise hareketleri tanimlamak icin acilari 0 ile 100 arasina sikistiriyoruz. normalde 180-260 arasi oluyor.
        # per = np.interp(angle, (185, 245), (0, 100))
        # print(angle)
    
    
    
        # ziplama hareketi icin
        
        angle = findAngle(img, 23, 25, 27, lmList)
        per = np.interp(angle, (65, 145), (0, 100))
        
        
        #burada dir ile hareketi bitiriyp bitirmedigini takip sayiyoruz.
        #count ile de hareketi tam yapip yapmadigina bakiyoruz yukardan baslayip asagiya indiginde 0.5 yukari ciktiginda
        #0.5 ekliyoruz, boylelikle kac tane tam hareket yaptigini sayiyoruz.
        if per == 100:
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            if dir == 1:
                count += 0.5
                dir = 0  
                
        print(count)
        
        #yukardaki saydiklarimizi burada ekrana bastiriyoruz.
        cv2.putText(img, str(int(count)), (45,125), cv2.FONT_HERSHEY_PLAIN, 10, (255,0,0), 10)
    
    cv2.imshow("img", img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        

cap.release()  # Kamerayı serbest bırak
cv2.destroyAllWindows()  # Tüm penceleri kapat






























































