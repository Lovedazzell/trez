
from django.contrib import admin
from django.urls import path, include , re_path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('core.urls')),


    # app urls
    path('auth/',include('authentication.urls')),
    path('apis/',include('apis.urls')),
    path('intg/',include('intg.urls')),
    path('suad/',include('superadmin.urls')),
    # path('intg/',include('intg.urls')),

    # url for  celery work
    re_path(r'^celery-progress/', include('celery_progress.urls')),  

    # this url for django rest framwork tasks
    path('api-auth/', include('rest_framework.urls')),

    # social authentication task
    path('accounts/', include('allauth.urls')),
]
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)   
urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)