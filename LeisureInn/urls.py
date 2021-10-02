"""LeisureInn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('chat/', include('chat.urls', namespace='chat')),
    
    path('admin/', admin.site.urls),
    
    # 3rd party urls
    path('accounts/', include('allauth.urls')), ## django-allauth url for user management
    path('messages/', include("pinax.messages.urls", namespace="pinax_messages")), # pinax url
    
    
    path('pages/', include('pages.urls', namespace='pages')),
    path('', include('rooms.urls', namespace='rooms')),
    path('book/', include('bookings.urls', namespace='bookings')),
    path('payment/', include('payments.urls', namespace='payments')), 
    path('guest_reservations/', include('guest_reservations.urls', namespace='guest_reservations')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Leisure Inn Admin"