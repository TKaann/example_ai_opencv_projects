import cv2
import pickle
import numpy as np


#kutuphaneleri import ediyoruz.


#algoritmamizi burada yaziyoruz simdi

#siyahlar ve beyazlari check edecek, dolu mu bos mu onlara bakicak bu fonksiyonumuz.
def checkParkSpace(imgg):
    spaceCounter = 0
    
    for pos in posList:
        x, y = pos
        
        #resmi bolme islemi yapiyoruz. y den y + height - x ten x + width e kadar boluyoruz.
        img_crop = imgg[y: y + height, x:x + width]
        
        #sifir olmayanlari hesapliyoruz.
        #buradaki ana mantik beyaz ve siyah oldugu icin renk 255 e ne kadar yakinsa beyaz 0 a ne kadar yakinsa siyah
        #yani burada isaretledigimiz kutucuklar siyah mi beyaz mi onun ayristirmasini yapiyoruz.
        count = cv2.countNonZero(img_crop)
        
        # print("count: ", count)
        
        #simdi burada ise isretledigmiz kutucuklarin icindeki renk eger 150 den az ise spacecounteri 1 artiriyoruz.
        #150 den az olmasi bize siyah oldugunu gosteriyor. yani 150 bizim esik degerimiz. 150 den fazlaysa yani beyaz
        #orada araba oldugunu anliyoruz.
        if count < 150:
            color = (0, 255, 0)
            spaceCounter += 1
        else:
            color = (0, 0, 255)
        
        #burada ise siyah beyaz degil ilk resmimiz uzerinde dolu veya bos oldugunu belirtmek icin
        #doluysa kutucuk kirmizi olacak bossa kutucuk yesil olacak sekilde kutucuk renklendirmelerini yapiyoruz.
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, 2) 
        
        #burada kutucuklarin icinde kordinatlarini yazdirdik.
        cv2.putText(img, str(count), (x, y + height - 2), cv2.FONT_HERSHEY_PLAIN, 1,color,1)
    
    #burada ise ne kadar bos ne kadar dolu yer oldugunu yaziyoruz.
    cv2.putText(img, f"Free: {spaceCounter}/{len(posList)}", (15,24), cv2.FONT_HERSHEY_PLAIN, 2,(0,255,255),4)

width = 27
height = 15

cap = cv2.VideoCapture("video.mp4")

#park yerleri belirledigimiz dosyamizi yukluyoruz.
with open("CarParkPos", "rb") as f:
    posList = pickle.load(f)

while True:
    success, img = cap.read()
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   #siyah beyaz videoda calisacagimiz icin grayscale e cevirdik.
    imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)   #videomuzdaki detaylari azaltmak icin gaussianblur (gurultu) ekliyoruz.
    #burada ise threshold ekliyoruz yani kontrast yapiyoruz. araclar beyaza zemin siyaha donuyor burada.
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    #arac ustunde zeminle ayni sekilde siyah rekler oldu onu azaltmak icin medianblur ekliyoruz.
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    #detaylari (siyah ve beyazlari) araclarin beyazliklarini biraz daha kalinlastirmak icin dilate ekliyoruz.
    imgDilate = cv2.dilate(imgMedian, np.ones((3,3)), iterations = 1)
    
    #simdi dilate islemini de yaptigimiza gore elimizde artik siyahlar ve beyazlar var. siyahlar bos beyazlar dolu
    
    
    #bruada fonksityonumuzda dilate ettigimiz gorseli veriyoruz. ona gore bos dolu sayimini yapiyor eger bunu threshold yaparsak
    #o zaman yukardaki piksel hesaplamalarini da degistirmemiz gereklidir. (fonksiyonun basinda yazdigimiz.)
    checkParkSpace(imgDilate)
    
    cv2.imshow("img", img)
    # cv2.imshow("img_gray", imgGray)
    # cv2.imshow("imgBlur", imgBlur)
    # cv2.imshow("imgThreshold", imgThreshold)
    # cv2.imshow("imgMedian", imgMedian)
    # cv2.imshow("imgDilate", imgDilate)
    cv2.waitKey(50)
    if cv2.waitKey(50) & 0xFF == ord('q'):
        break
        

cap.release()  # Kamerayı serbest bırak
cv2.destroyAllWindows()  # Tüm penceleri kapat































































