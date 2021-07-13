from django.shortcuts import render, HttpResponse, redirect


from django.core.files import File
import os
import re
from .models import Picture, Palette
from django.conf import settings
from datetime import datetime

def index(request):
    return render(request, 'coloring/index.html', {'photos':Picture.objects.all().order_by('-date_modified')})
def demo(request):
    return render(request, 'coloring/demo.html')

#<<<<<<< HEAD
def homepage(request, category):
    #context = {'pictures': Picture.objects.filter(main=True).order_by('item')}
    categories = list(set([pic.category for pic in Picture.objects.all()]))
    return render(request, 'coloring/homepage.html', {'photos':Picture.objects.filter(category=category),'categories':categories})


    #return render(request, 'coloring/homepage.html', {'photos':Picture.objects.all()})

#=======
#def homepage(request,category):
    #context = {'pictures': Picture.objects.filter(main=True).order_by('item')}
 #   category = list(set([pic.category for pic in Picture.objects.all()]))
 #   return render(request, 'coloring/homepage.html', {'photos':Picture.objects.filter(category=category),'categories':category})

#>>>>>>> e754e7605856b652df5bcab09a54d2926f20b96d


#def gallery(request):
 #   pic = Picture.objects.all()[0]
  #  return render(request,'coloring/gallery.html',context={"pictures":Picture.objects.all()})

def gallery(request):
    pic = Picture.objects.all()[0]
    return render(request,'coloring/gallery.html',context={"pictures":Picture.objects.filter(edited=True).order_by('-date_modifed')})

# def canvas(request,id,force=False):
#     files = os.listdir(STATIC_IMAGE_PATH)
#     exactMatch = [re.search(str(id)+"\.svg",x) for x in files]
#     partialmatch = [re.search(str(id)+"\..+",x) for x in files]
#     if any(exactMatch) and not force:
#         return render(request,'coloring/canvas.html',{"imagePath":STATIC_IMAGE_PATH_TEMPLATE+str(id)+".svg"})
#     elif any(partialmatch):
#         convert(request,list(filter(lambda x: x,partialmatch))[0].string)
#         return render(request,'coloring/canvas.html',{"imagePath":STATIC_IMAGE_PATH_TEMPLATE+str(id)+".svg"})
#     return HttpResponse("File does not exist")

def canvas(request,id,paletteName='Basic Colors'):
    pic = Picture.objects.get(pk=id)
    path =settings.MEDIA_ROOT + "/"+pic.photo.name
    if path.split("/")[-1] != str(id)+".svg" :
        # if path.split(".")[-1] != "svg":
        intermediatePath = settings.MEDIA_ROOT+"/"+str(id) +".pgm"
        outputPath = settings.MEDIA_ROOT+"/"+str(id)+"temp.svg"
        os.system('convert ' + path+ " " + intermediatePath)
        os.system('potrace ' + intermediatePath +" -s --opaque -o " + outputPath)
        os.system('rm ' + settings.MEDIA_ROOT + "/" + str(id)+".svg")
        pic.photo.save(str(id)+".svg",File(open(outputPath,'rb')))
        os.system('rm ' + intermediatePath)
        os.system('rm ' + path)
        os.system('rm ' + outputPath)
        # else:
        #     os.rename(path,settings.MEDIA_ROOT+"/"+)
    colors = []
    if paletteName == 'Blank':
        colors =['#FFFFFF']*8
    else:
        try:
            colors = Palette.objects.get(pk=paletteName).colors.split(",")
        except:
            colors=['#FFFFFF']*8
            paletteName='Blank'
    return render(request,'coloring/canvas.html',{"id":id,"imagePath":pic.photo.url,'colors':colors,'paletteName':paletteName,'paletteNames':[p.name for p in Palette.objects.all()]})


def upload(request):
    return render(request,'coloring/upload.html')

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
def savePalette(request):
    paletteName = request.POST.get("paletteName")
    colors = request.POST.get("colors")[:-1]
    print(paletteName,colors)
    try:
        pal  = Palette.objects.get(pk=paletteName)
        pal.colors=colors
        pal.save()
    except:
        pal = Palette(name=paletteName,colors=colors)
        pal.save()
    return HttpResponse("Success")

def saveImage(request):
    print("save Image request received")
    id = request.POST.get('id')
    content=request.POST.get('content')
    # print(content)
    path = settings.MEDIA_ROOT +"/"+str(id)+".svg"
    try:
        pal=Picture.objects.get(pk=id)
        print(pal.date_modified)
        my_file = open(path, "w")
        my_file.write(content)
        my_file.close()
        pal.edited=True
        pal.save()
        return HttpResponse('Success')

    except Exception as e:
        print(e)
        return HttpResponse('Error')
def uploadImage(request):
    file = request.FILES['file']
    category= request.POST.get("category")
    pic = Picture(category=category,photo=file)
    pic.save()
    return redirect('index')
