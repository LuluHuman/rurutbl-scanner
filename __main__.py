doOnly = False #! Page number of file in PDF

import os
import shutil
import math
import pytesseract
from convert import convert
from procImg import procImg
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
convert()

if not (doOnly):
    maindir = os.listdir("./pages")
    for weeks in maindir:
        week = os.listdir("./pages/"+weeks)
        for classes in week:
            classdir = ("./pages/"+weeks+"/"+classes)
            if (weeks == "odd"):
                procImg(classdir, False, classes.replace(".jpg",""))
            else:
                procImg(classdir, True, classes.replace(".jpg",""))
else:
    weeks = os.listdir("./pages/")
    for week in weeks:
        if (weeks == "odd"):
            procImg("./pages/"+week+"/"+str(math.floor(24/2))+".jpg", True, str(math.floor(24/2)))
        else:
            procImg("./pages/"+week+"/"+str(math.floor(24/2))+".jpg", False, str(math.floor(24/2)))

shutil.rmtree("./pages")