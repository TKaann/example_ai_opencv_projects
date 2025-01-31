import cv2
import numpy as np


#gerekli kutuphanelri import ediyoruz.
#burada klasik goruntu isleme tekniklerini kullaniyoruz mediapipe i kullanmicaz.




def region_of_interest(image, vertices):    #kesme maskeleme islemlerini yapmak icin fonksiyon.
    #bu fonksiyon icinde maskemele islemerini yapiyoruz, asagidaki kodlar maskeleme islemleri.
    
    mask = np.zeros_like(image)
    
    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image



def drawLines(image, lines):     #process dekii belirledigimiz lineleri burda artik cizdiriyoruz.
    
    image = np.copy(image)
    blank_image = np.zeros((image.shape[0], image.shape[1],3),dtype = np.uint8)
    
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(blank_image, (x1,y1),(x2,y2),(0,255,0),thickness = 10)
            #x1, y1 den x2,y2 ye kadarki yerledeki line cizdirme islemini yaptiriyoruz. 
            #sonrasinda orijinal videomuzun ustune cizdiriyoruz.
        
    image = cv2.addWeighted(image, 0.8, blank_image, 1, 0.0)
    return image

def process(image):
    height, width = img.shape[0], img.shape[1]       #videomuzun yukseklik ve genislik bilgilerini girdik.
    
    region_of_interest_vertices = [(0, height), (width/2, height/2), (width, height)]
    #burada bizim yaptigimiz sey sol alttan videonun merkezine ordan sa sag alta kadarki kismi almak.
    #geri kalani kestiik. yolun soldakii ciizgisini ve ortadaki cizgiisii kaldi.
    #buradki region of interesetleri maskeleme yapmak icin kullanicaz.
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)    #gray scale a cevirdik.
    canny_image = cv2.Canny(gray_image, 250, 120)         #line  detection icin cannt fonksiyonundan faydalaniyoruz.
    #burdaki parametreleri ise ana cizgimize gore ayarliyoruz.
    
    cropped_image = region_of_interest(canny_image, np.array([region_of_interest_vertices], np.int32))
    
    lines = cv2.HoughLinesP(cropped_image,
                            rho = 2, 
                            theta = np.pi/180, 
                            threshold = 200, 
                            lines = np.array([]),
                            minLineLength = 150, 
                            maxLineGap = 4)
    #burada ise videodakii duz cizgileri tespit etmek icin HoughLinesP fonksiyonunu kullandik.
    #burada rho,theta,threshold, degerleri default girdigimiz degerler. miin ve max bizim icin onemli.
    #Minline onemli br parametre diger projelerde ayri kullanimlari olan biir sey. adi ustunde tespit edecegi min line in uzunlugu.
    #maxLineGap de onemlidir o ise, 2 tane line arasinda kucuk bir gap varsa bu aslinda 2 tane line oldugu anlamina gelir.
    #burda da o gap in boyutunu taniimliyoruz. ne kadar bir gapten sonra 2 tane cizgi var onun ozelligi.
    #tanimlanilan linegapten kucukse 2 line o tek bir line dir onu tek line yap onemseme diyoruz.
    
    
    
    # print(lines)
    imageWithLine = drawLines(image, lines)
    return imageWithLine

cap = cv2.VideoCapture("video2.mp4")      #videomuzu aktariyoruz
 
while True:
    success, img = cap.read()       #videomuzu ice aktardik
    img = process(img)             #imgmizi process fonksiyonumuza yolluyoruz ve ordaki islemleri yaptirtiyoruz
                                    #gray scale, crop vb falan.
    if success:
        cv2.imshow("img", img)     #eger videodan veri cekme basarili oluyorsa videoyu oynatmaya devem et.
        cv2.waitKey(20)
    else: break                  #video bittikten sonra hata almamak icin succesin else durumunda break yapiyoruz
                                #donguden cikiyoruz ve alttaki release ve destroyAllWindows fonksiyonlarina geciyoruyz.
     
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
        

cap.release()  # Kamerayı serbest bırak
cv2.destroyAllWindows()  # Tüm penceleri kapat
























































