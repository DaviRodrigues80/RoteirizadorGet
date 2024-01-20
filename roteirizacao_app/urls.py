from django.urls import path
from .views import calcular_resumo, lista_enderecos, adicionar_endereco, imprimir_rota

urlpatterns = [
    path('', lista_enderecos, name='lista_enderecos'),
    path('adicionar/', adicionar_endereco, name='adicionar_endereco'),
    path('imprimir_rota/', imprimir_rota, name='imprimir_rota'),
    path('calcular_resumo/', calcular_resumo, name='calcular_resumo'),
   
]
