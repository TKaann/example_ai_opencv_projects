import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot



#gerekli kutuphsnelerimizi import ediyoruz. facemeshmodule zaten bildigimiz face mesh islemi. gozleri bulacagimiz kutuphane.
#cvzone ise cok kullanisli bir kutuphanedir.
#liveplot ise bize canli bir plot olusturuyor ve bu sayede daha iyi bir threshold modeulu yapabilicez.



cap = cv2.VideoCapture("video2.mp4")
detector = FaceMeshDetector()      #face mesh detected yaptik
plotY = LivePlot(540, 360, [10, 60])     #canli plotumuz 540 istege bagli ama 360 degeri olmasi gereken min size.
                            #eger 360 dan daha kucuk olursa hata verir. digerleri ise y eksenindeki plot degerleri

idList = [22, 23, 24, 26, 110, 157, 158, 159, 160, 161, 130, 243]
#bunlar meshdeki gozlerin id leri, bize gore sol kisi icin ise sag gozun id leri.
color = (0,0,255)
ratioList = []
counter = 0
blickCounter = 0

while True:
    success, img = cap.read()
    img, faces = detector.findFaceMesh(img, draw = False)     #resmimizin icindeki mesh i buluyor.
    
    if faces:
        face = faces[0]
        
        for id in idList:
            cv2.circle(img, face[id], 5, color, cv2.FILLED)    #gozun etrafina kirmizi cizgiler cizdiriyoruz.
        
        #burada ise gozun ustunu ve altini belirliyoruz. cunku gozun kirpma islemini ust ve altin mesafesine gore yapicaz.
        leftUp = face[159]
        leftDown = face[23]
        leftLeft = face[130]
        leftRight = face[243]
        
        lengthVer, _ = detector.findDistance(leftUp, leftDown)    #ust ve alt noktalar
        lengthHor, _ = detector.findDistance(leftLeft, leftRight)  #sag ve sol noktalar
        
        cv2.line(img, leftUp, leftDown, (0,255,0),3)   #burada gozun ust ve alti arasinda cizgi cizdiriyoruz.
        cv2.line(img, leftLeft, leftRight, (0,255,0),3)   #burada ise sagi ve solu arasinda cizgi cizdiriyoruz.
        #bu bize ust alt ve sag sol arasindaki mesafeleri veriyor.
        
        
        
        #burada ise gozu kirpmis mi kirpmamis mi yuzdelik hesap yapiyoruz.
        ratio = int((lengthVer/lengthHor)*100)
        ratioList.append(ratio)
        
        #bruada raitolistimizi sinirliyoruz. 3 den buyuk olursa ilk elemanini cikartiyoruz.
        #bu sayede ratioliste sadece son 3 eleman  ekleniyor. diger turlu cok fazla veri donuyor ve ortalama belirledigimiz
        #35 in altinda dusmuyor. biz burada listemizin % ortalamasina gore kirpip kirpmadigina bakiyoruz.
        if len(ratioList)>3:
            ratioList.pop(0)       
        
        ratioAvg = sum(ratioList)/len(ratioList)
        print(ratioAvg)
        
        #ratiomuzun oranina gore goz kirtmayi sayiyoruz.
        if ratioAvg < 35 and counter == 0:
            blickCounter += 1
            color = (0,255,0)
            counter = 1
        if counter != 0:
            counter += 1
            if counter > 10:
                counter = 0
                color = (0,0,255)
        
        cvzone.putTextRect(img, f'Blink Count: {blickCounter}', (50,100), colorR = color)
        
        #burada ise bir ratio grafigi ekliyoruz ve bizim ayarladigimz threshold ustune cikip cikmadigina bakiyoruz.
        imgPlot = plotY.update(ratioAvg, color)
        img = cv2.resize(img, (640,360))
        imgStack = cvzone.stackImages([img, imgPlot], 2,1)

        
    if success:
        cv2.imshow("img", imgStack)     #eger videodan veri cekme basarili oluyorsa videoyu oynatmaya devem et.
        cv2.waitKey(1)
    else: break
                              
     
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        

cap.release()  # Kamerayı serbest bırak
cv2.destroyAllWindows()  # Tüm penceleri kapat






































































