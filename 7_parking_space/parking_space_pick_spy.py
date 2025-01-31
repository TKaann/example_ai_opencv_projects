import cv2
import pickle
#pickle kutuphanesi sayesinde isaretlemis oldugumuz resmi kaydediyoruz. 
#park pozisyonlarini kaydediyoruz ve resmin ustune otomatik olarak isleniyor.


#gerkli kutuphaneler import islemi



width = 27
height = 15

try:
    #burda ise alttaki poListimiz tekrardan sifirlanmasin diye Carparkpos dosyasinin icine yazdiriyoruz.
    with open("CarParkPos", "rb") as f:
        posList = pickle.load(f)
except:
    posList = []

def mouseClick(events, x, y, flags, params):
    #mouse ile tiklamamizi ve tikladigimiz yerleri (kordinatlari) poList listesine eklememizi yapiyoruz.
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
        
    #buraya da yanlis tikladigimiz yerleri sag click ile tiklayinca kaldirmayi yapiyoruz.
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
                
    #burda da her seferinde tek tek park yerlerine tiklamak yerine tikladigimiz yerleri kaydediyoruz.
    with open("CarParkPos","wb") as f:
        pickle.dump(posList, f)

while True:
    img = cv2.imread("first_frame.png")
    
    #yukardaki poListten aldigimiz kordinatlarin oldugu yere kutucuk cizdiriyoruz.
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255,0,0),2)
    # print("poslist: ",posList)
    
    cv2.imshow("img", img)
    cv2.setMouseCallback("img", mouseClick)
    cv2.waitKey(1)



























































