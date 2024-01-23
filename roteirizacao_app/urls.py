from django.urls import path
from .views import lista_enderecos, adicionar_endereco, imprimir_rota

urlpatterns = [
    path('', lista_enderecos, name='lista_enderecos'),
    path('adicionar/', adicionar_endereco, name='adicionar_endereco'),
    path('imprimir_rota/', imprimir_rota, name='imprimir_rota'),
    
   
]
