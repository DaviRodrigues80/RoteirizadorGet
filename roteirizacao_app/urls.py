from django.urls import path
from .views import lista_enderecos, adicionar_endereco

urlpatterns = [
    path('', lista_enderecos, name='lista_enderecos'),
    path('adicionar/', adicionar_endereco, name='adicionar_endereco'),
]
