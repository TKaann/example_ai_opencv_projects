import cv2
import mediapipe as mp
import time


#gerkli kutuphanelerimizi import ettik




mpPose = mp.solutions.pose
pose = mpPose.Pose()

mpDraw = mp.solutions.drawing_utils

cap = cv2.VideoCapture("video1.mp4")
# cap = cv2.VideoCapture(0)
#burasi ise bizim kameramizi aciyor.


#videomuzu import ediyoruz


pTime = 0


while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    print(results.pose_landmarks)
    
    #video uzerindeki noktalari cikti olarak aliyoruz.
    
    
    if results.pose_landmarks:   #if kullanmamizin sebebi landmarks 0 ise girmeyecek ve none dondurecek
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        
        
        #simdi istedigimiz noktalari seciyoruz
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, _ = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h)   #x ve y kordinatlarini elde ediyoruz
            
            if id == 13:    #id si 13 olan noktaya noktalar atiyoruz
                cv2.circle(img, (cx, cy), 5, (255,0,0),cv2.FILLED)
                
    
    #fps hesaplayalim
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime    
    
    cv2.putText(img, "FPS: "+str(int(fps)), (10,65), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)
    
    
    cv2.imshow("img", img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        

cap.release()  # Kamerayı serbest bırak
cv2.destroyAllWindows()  # Tüm penceleri kapat

























































































