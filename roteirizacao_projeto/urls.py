from django.contrib import admin
from django.urls import path, include
from roteirizacao_app.views import signup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('roteirizacao_app.urls')),
    path('signup/', signup, name='signup'),
]

