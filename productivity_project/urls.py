from django.contrib import admin
from django.urls import path, include
from productivity_tools.views import homePage

urlpatterns = [
    path('', homePage, name='home'),  
    path('admin/', admin.site.urls),  
    path('user/', include('user.urls')),  
    path('productivity_tools/', include('productivity_tools.urls')),
]
