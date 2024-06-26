import easyocr

import cv2
reader = easyocr.Reader(['en'], gpu=True)
def ocr_image(img,coordinates):
    x,y,w, h = int(coordinates[0]), int(coordinates[1]), int(coordinates[2]),int(coordinates[3])
    img = img[y:h,x:w]

    gray = cv2.cvtColor(img , cv2.COLOR_RGB2GRAY)
    result = reader.readtext(gray)
    text = ""

    for res in result:
        if len(result) == 1:
            text = res[1]
        if len(result) >1 and len(res[1])>6 and res[2]> 0.2:
            text = res[1]

    
    return str(text)