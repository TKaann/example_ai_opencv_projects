import cv2
import mediapipe as mp


#gerekli kutuphanelerin import islemi


cap = cv2.VideoCapture("video3.mp4")    #videoyu ice aktariyoruz

mpFaceDetection = mp.solutions.face_detection    #Mediapipe kutuphanesinde olan face detection modulunu cagirdik
faceDetection = mpFaceDetection.FaceDetection(0.20)    #facedetection modulunu cagirdik icine istedigimiz parametreyi giriyoruz.
#eger buradaki parametreyi 0 a ne kadar yakinlastirirsak o kadar fazla detect etmeye calisacak ve alakasiz seyleri
#sanki yuzmus gibi algilayip bissuru sacma kutucuk cikartacak.
#eger 100 e yaklastirirsakda takibi cok yapacak ve detect islemi yapmayacak. bu degeri kendimiz iyi bir deger secmeliyiz. 0.20

mpDraw = mp.solutions.drawing_utils

while True:
    success, img = cap.read()     #temel gorsellestirmeleri yapiyoruz.
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   #BGR dan RGB ye ceviriyoruz
    
    results = faceDetection.process(imgRGB)
    
    # print(results.detections)
    if results.detections:
        for id, detection in enumerate(results.detections):      #eger bir detecyion varsa kendisini ve id sini aliyoruz.
            
            bboxC = detection.location_data.relative_bounding_box    #bounding box ekliyoruz
        #bruadaki kodda sadece tespit edilen nesnenin kordinat olarak tespiti yapiliyor, sol ust sag ust sag alt sol alt gibi
        #sonrasinda sol ust koseyi w ve h ile carpilarak nesnenin pixel boyutunu buluyoruz
            
            
            # print(bboxC)
            h, w, _ = img.shape   #hight ve width ekliyoruz, color eklemiyoruz o yuzden _ de birakiyoruz.
            
            bbox = int(bboxC.xmin*w), int(bboxC.ymin*h), int(bboxC.width*w), int(bboxC.height*h)
    #sonrasinda nesnenin pixel boyutunu buldukran sonra sol ust kosesini referans alarak buldugumuz piksel boyutu oturtuyoruz
            #burasi bize x y ve width ve height donduruyor yani bbox donduuryor.
            #print(bbox) yaparak gorebilirsin.
            
            
            cv2.rectangle(img, bbox, (0,255,255),2)    #rectangele cizdirdigimiz zaman otomaik olarak img ve kutuyu aliyor
                                                        #sadece rengini yaziyoruz biz de
    
    cv2.imshow("img", img)
    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        

cap.release()  # Kamerayı serbest bırak
cv2.destroyAllWindows()  # Tüm penceleri kapat




























































