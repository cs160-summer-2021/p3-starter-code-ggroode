from django.urls import path,re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('demo', views.demo, name='demo'),
    path('', views.index, name='index'),
    path('new_interaction', views.index, name='new_interaction'),
    path('convert/<str:filename>',views.convert,name="convert"),
    path('canvas/<int:id>',views.canvas,name='canvas'),
    path('homepage', views.homepage, name='homepage'),

    
    path('canvas/<int:id>/<str:paletteName>',views.canvas,name='canvas'),
    # path('canvas2/<int:id>',views.canvas2,name='canvas2'),
    path('gallery',views.gallery,name="gallery"),
    path('savePalette',views.savePalette,name='savePalette'),
]
