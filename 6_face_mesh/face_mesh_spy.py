import cv2
import time
import mediapipe as mp

#kuutphanelerin import islemi



cap = cv2.VideoCapture("video3.mp4")    #video ice aktarmayi yaptik

mpFaceMesh = mp.solutions.face_mesh     #mediapipe kutuphanesinden face mesh metodunu aliyoruz.
faceMesh = mpFaceMesh.FaceMesh(max_num_faces = 1)    #burda da nesneyi cagirdik fonksiyonu cagiriyoruz.
mpDraw = mp.solutions.drawing_utils        #draw islemlerini yapiyoruz
drawSpec = mpDraw.DrawingSpec(thickness = 1, circle_radius = 1)   #draw speclerini belirliyoruz
#bu neden onemli cunku nesnemiz uzaktaysa mesh cok yogun olacak yakindaysa cok ayrik olacak o yuzden ozellikleri ayarliyoruz.

pTime = 0
while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    #BGR dan RGB ye ceviriyoruz
    results = faceMesh.process(imgRGB)   #landmarklari olusturduk. yuz oldugu zaman kordinatlar olmadigi zaman none donuyor.
    print(results.multi_face_landmarks)
    
    if results.multi_face_landmarks:   #eger none degilse gorsellestirme yapicaz.
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_TESSELATION, drawSpec, drawSpec) # FACEMESH_CONTOURS
            #burada aslinda mesh islemini gerceklestiriyoruz, yuze mesh cizdiriyoruz. 
            #drawspec olarak da kendi ayarladigimiz drawspec ayarlarini giriyoruz.
    
    
        #burasi ise kordinat belirlemek icin yaptigimiz islemler, duygu analizi, dudak, agiz, goz gibi seylerde kullanilir.
        for id, lm in enumerate(faceLms.landmark):
            h, w, _ = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            print([id, cx, cy])
    
    #burada ise fps hesapliyoruz.
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, "FPS: "+str(int(fps)), (10,65), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)  
    
    cv2.imshow("img", img)    #gorsellestirmesini yapiyoruz.
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        

cap.release()  # Kamerayı serbest bırak
cv2.destroyAllWindows()  # Tüm penceleri kapat




































































