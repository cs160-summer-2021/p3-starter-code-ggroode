from django.shortcuts import render, HttpResponse


from django.core.files import File
import os
import re
from .models import Picture
from django.conf import settings

def index(request):
    return render(request, 'coloring/index.html', {'photos':Picture.objects.all()})
def demo(request):
    return render(request, 'coloring/demo.html')

def homepage(request):
    context = {'pictures': Picture.objects.filter(main=True).order_by('item')}
    return render(request, 'coloring/homepage.html', context) 
        #{'photos':Picture.objects.all()})
 

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

def canvas2(request,id,force=False):
    print("Canvas 2- Request Recieved")
    pic = Picture.objects.get(pk=id)
    print(pic.id)
    print(pic.pk)
    path =settings.MEDIA_ROOT + "/"+pic.photo.name
    print(path)
    print(pic.photo.url)
    print("Canvas 2- Object loaded")
    if path.split(".")[-1] != "svg":
        print("Canvas 2- Object Updating Begining")
        intermediatePath = settings.MEDIA_ROOT+"/"+str(id) +".pgm"
        outputPath = settings.MEDIA_ROOT+"/"+str(id)+"temp.svg"
        print(intermediatePath)
        print(outputPath)
        os.system('convert ' + path+ " " + intermediatePath)
        print("Canvas 2- First Conversion")
        os.system('potrace ' + intermediatePath +" -s --opaque -o " + outputPath)
        print("Canvas 2- Seconds Conversion")
        pic.photo.save(str(id)+".svg",File(open(outputPath,'rb')))
        os.system('rm ' + intermediatePath)
        os.system('rm ' + path)
        os.system('rm ' + outputPath)
    #return render(request,'coloring/canvas.html',{"imagePath":"/../"+settings.MEDIA_ROOT + "/" + str(id)+".svg"})
    return render(request,'coloring/canvas.html',{"imagePath":pic.photo.url})

STATIC_IMAGE_PATH_TEMPLATE="/static/coloring/images/"
STATIC_IMAGE_PATH="coloring/static/coloring/images/"
def convert(request,filename):
    name,type = filename.split(".")
    path = STATIC_IMAGE_PATH+filename
    intermediatePath = STATIC_IMAGE_PATH+name+ ".pgm"
    outputPath = STATIC_IMAGE_PATH+name+".svg"
    os.system('convert ' + path + " " + intermediatePath)
    os.system('potrace ' + intermediatePath +" -s --opaque -o " + outputPath)
    return HttpResponse("File converted successfully")
    # image = Image.open(path)
    # imageArr = np.asarray(image)
    # bitmap = pt.Bitmap(imageArr)
    # path = bitmap.trace()
