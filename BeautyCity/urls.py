from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from BeautyCity import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('AppHome.urls')),
    path('accounts/', include('django.contrib.auth.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
