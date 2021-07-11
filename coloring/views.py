from django.shortcuts import render, HttpResponse
#from PIL import Image
#import numpy as np
#import potrace as pt
import os
import re

def index(request):
    return render(request, 'coloring/demo.html')

def canvas(request,id,force=False):
    files = os.listdir(STATIC_IMAGE_PATH)
    exactMatch = [re.search(str(id)+"\.svg",x) for x in files]
    partialmatch = [re.search(str(id)+"\..+",x) for x in files]
    if any(exactMatch) and not force:
        return render(request,'coloring/canvas.html',{"imagePath":STATIC_IMAGE_PATH_TEMPLATE+str(id)+".svg"})
    elif any(partialmatch):
        convert(request,list(filter(lambda x: x,partialmatch))[0].string)
        return render(request,'coloring/canvas.html',{"imagePath":STATIC_IMAGE_PATH_TEMPLATE+str(id)+".svg"})
    return HttpResponse("File does not exist")

STATIC_IMAGE_PATH_TEMPLATE="/static/coloring/images/"
STATIC_IMAGE_PATH="coloring/static/coloring/images/"
def convert(request,filename):
    name,type = filename.split(".")
    path = STATIC_IMAGE_PATH+filename
    intermediatePath = STATIC_IMAGE_PATH+name+ ".pgm"
    outputPath = STATIC_IMAGE_PATH+name+".svg"
    os.system('convert ' + path + " --flatten " + intermediatePath)
    os.system('potrace ' + intermediatePath +" -s --opaque -o " + outputPath)
    return HttpResponse("File converted successfully")
    # image = Image.open(path)
    # imageArr = np.asarray(image)
    # bitmap = pt.Bitmap(imageArr)
    # path = bitmap.trace()
