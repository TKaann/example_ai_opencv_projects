#hand tracking dedigimiz islem 2 ana bolumden olusuyor. 1- palm detector 2- hand landmarks olarak adlandiriliyor.
#palm detector: elimizin tespitinin gerceklesmesi
#hand landmarks: eklem yerlerini kirmizi bir yuvarlakla belirleyip kirmizi yerlerin konumunu x y z olarak cikartiyor.
#hand landmarksta 21 tane eklem yerimizin isretlemesini yapmis olucaz. bu sayede elin takibini gerceklestiriyoruz.

import cv2
import time   #fps takibi icin
import mediapipe as mp    #mediapipe projelerimizde kullanacagimiz google tarafindan olusturulan bir kutuphanedir.

cap = cv2.VideoCapture(0)    # 0 olmasi bilgisayarimizdaki mevcut kamerayi kullan demek.

#simdi hang tracking icin gerekli olan fonksiyonlari yazalim.

mpHand = mp.solutions.hands

hands = mpHand.Hands()

mpDraw = mp.solutions.drawing_utils   #bu bizim elimizde cizgiler olmasin sagliyor.
#bu hands fonksiyonunun icinde farkli farkli parametreler var, max hands gibi gibi bunlari kendi projelerimizi yaparken
#okuyup faydalanmamiz gerekiyor, isimize yarayanlari bulup deneyerek optimum hale getirmemiz gerekir.
#buradaki hands modulu de RGB kullaniyor o yuzden fonksiyonumuzu RGB yapmamiz lazim
pTime = 0
cTime = 0
while True:
    success , img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    results = hands.process(imgRGB)         #hands modulunu kullanabilmek icin process modulunu cagirdik.
    print(results.multi_hand_landmarks)    #burada detectionumuz olmaya basliyor, multi_hand_landmarks sayesinde
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHand.HAND_CONNECTIONS)
            
            for id, lm in enumerate(handLms.landmark):   
                #burada x y z yi dondurup lm e atiyor eklemin hangisi oldugunu da id ye. id hangi eklem oldugunu soyluyor.
                
                #print(id,lm)
                
                h, w, c = img.shape  #kordinatlari belirlemek icin kullaniyoruz.
                cx, cy = int(lm.x*w), int(lm.y*h) #simdi bunlari kordinat sistemlerine ceviriyoruz cx ve cy ye.
                
                #bilek
                if id == 4:
                    cv2.circle(img, (cx,cy), 9, (255,0,0), cv2.FILLED)
                    
                    
    #fps hesaplama bizim icin neden onemli: algoritmamizin ne kadar hizli calistigini gormek icin.
    cTime = time.time()
    fps = 1 / (cTime- pTime)
    pTime = cTime
    
    cv2.putText(img, "Fps: " +str(int(fps)), (10,75), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 5)
    
                
                
    
    cv2.imshow("img", img)
    cv2.waitKey(1)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # Kamerayı serbest bırak
cv2.destroyAllWindows()  # Tüm penceleri kapat






























































































