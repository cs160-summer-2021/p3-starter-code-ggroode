from django.urls import path,re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('', views.homepage, name='index'),
    path('canvas/<int:id>',views.canvas,name='canvas'),
    path('homepage',views.homepage,name='hompeage'),
    path('homepage/<str:category>', views.homepage, name='homepage'),
    path('canvas/<int:id>/<str:paletteName>',views.canvas,name='canvas'),
    # path('canvas2/<int:id>',views.canvas2,name='canvas2'),
    path('gallery',views.gallery,name="gallery"),
    path('savePalette',views.savePalette,name='savePalette'),
    path('saveImage',views.saveImage,name='saveImage'),
    path('uploadImage',views.uploadImage,name='uploadImage'),
    path('help',views.help,name='help'),
    path('clear',views.clear,name='clear')

]
