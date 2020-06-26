from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('sns/', include('sns.urls')),
    path('', include('sns.urls')),
    path('admin/', admin.site.urls),
]