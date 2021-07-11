from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
urlpatterns = [
    path('admin/', admin.site.urls),
    path('coloring/', include('coloring.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
