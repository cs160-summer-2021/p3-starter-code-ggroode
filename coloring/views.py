from django.shortcuts import render, HttpResponse, redirect


from django.core.files import File
import os
import re
from .models import Picture, Palette
from django.conf import settings
from datetime import datetime

def help(request):
    return render(request, 'coloring/help.html')

def homepage(request, category="Mandala"):
    #context = {'pictures': Picture.objects.filter(main=True).order_by('item')}
    categories = list(set([pic.category for pic in Picture.objects.all()]))
    pic1,pic2=Picture.objects.filter(edited=True).order_by('-date_modified')[:2]
    return render(request, 'coloring/homepage.html', {'photos':Picture.objects.filter(category=category),'categories':categories,'category':category,'pic1':pic1,'pic2':pic2})

def gallery(request):
    pic = Picture.objects.all()[0]
    return render(request,'coloring/gallery.html',context={"pictures":Picture.objects.filter(edited=True).order_by('-date_modified')})

def canvas(request,id,paletteName='Basic Colors'):
    pic = Picture.objects.get(pk=id)
    path =settings.MEDIA_ROOT + "/"+pic.photo.name
    newName = str(id)+".svg"
    if path.split("/")[-1] != newName :
        # if path.split(".")[-1] != "svg":
        intermediatePath = settings.MEDIA_ROOT+"/"+str(id) +".pgm"
        outputPath = settings.MEDIA_ROOT+"/"+str(id)+"temp.svg"
        os.system('convert ' + path+ " " + intermediatePath)
        os.system('potrace ' + intermediatePath +" -s --opaque -o " + outputPath)
        os.system('rm ' + settings.MEDIA_ROOT + "/" + str(id)+".svg")
        pic.photo.save(newName,File(open(outputPath,'rb')))
        os.system('rm ' + intermediatePath)
        os.system('rm ' + path)
        os.system('rm ' + outputPath)
        backupName=str(id)+"_backup.svg"
        os.system("scp " + settings.MEDIA_ROOT+"/"+newName + " " + settings.MEDIA_ROOT + "/" + backupName)
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
    return render(request,'coloring/canvas.html',{"pic":pic,'paletteName':paletteName,'paletteNames':[p.name for p in Palette.objects.all()],'colors':colors})


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
    print(request.FILES)
    file = request.FILES['files[]']
    print(file)
    category= request.POST.get("category")
    pic = Picture(category=category,photo=file)
    pic.save()
    return redirect('index')

def clear(request):
    print(request.POST)
    id = request.POST.get('id')
    print(id)
    pic = Picture.objects.get(pk=id)
    pic.edited=False
    pic.save()
    newName = str(id)+".svg"
    backupName=str(id)+"_backup.svg"
    os.system("scp " + settings.MEDIA_ROOT + "/" + backupName + " " + settings.MEDIA_ROOT+"/"+newName )
    return HttpResponse('Success')
