import html
import json
from urllib import request
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template import RequestContext
import soupsieve
from .models import Endereco, Viagem
from .forms import EnderecoForm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from io import BytesIO
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt  # Importe o decorador CSRF
from django.template.loader import render_to_string


def lista_enderecos(request):
    enderecos = Endereco.objects.all()
    return render(request, 'lista_enderecos.html', {'enderecos': enderecos})

def adicionar_endereco(request):
    if request.method == 'POST':
        form = EnderecoForm(request.POST)
        if form.is_valid():
            # Adiciona o endereço à tabela temporária (não salva no banco de dados)
            endereco_temporario = form.cleaned_data
            endereco_temporario['id_temporario'] = len(request.session.get('enderecos_temporarios', [])) + 1
            enderecos_temporarios = request.session.get('enderecos_temporarios', [])
            enderecos_temporarios.append(endereco_temporario)
            request.session['enderecos_temporarios'] = enderecos_temporarios

            return redirect('lista_enderecos')
    else:
        form = EnderecoForm()

    return render(request, 'adicionar_enderecos.html', {'form': form})

def imprimir_rota(request):
    if request.method == "POST":
        # Supondo que você esteja recebendo HTML como parte da requisição POST
        html = request.POST.get('html', '')

        # Use BeautifulSoup para analisar o HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Encontre o texto dentro da tag h1
        texto_h1 = soup.find('h1').string if soup.find('h1') else "H1 não encontrado"

        # Imprima o valor no terminal (para verificar no console)
        print(f"O valor da variável texto_h1 é: {texto_h1}")

        # Retorne a resposta renderizada com o texto_h1 como contexto
        return render(request, 'imprimir_rota.html', {'texto_h1': texto_h1})
    else:
        # Se a requisição não for POST, renderize a página normalmente
        return render(request, 'imprimir_rota.html')


def obter_numero_viagem_atual():
    # Obtenha o último número de viagem salvo no banco de dados
    ultima_viagem = Viagem.objects.order_by('-numero_viagem').first()

    if ultima_viagem:
        numero_viagem = ultima_viagem.numero_viagem + 1
    else:
        numero_viagem = 1

    return numero_viagem

def salvar_endereco(valor):
    # Verifique se o endereço já existe no banco de dados
    endereco_existente = Endereco.objects.filter(CEP=valor['CEP'], numero=valor['numero']).first()

    if not endereco_existente:
        # Salve o endereço se não existir
        Endereco.objects.create(
            CEP=valor['CEP'],
            LOGRADOURO=valor['logradouro'],
            NUMERO=valor['numero'],
            LATITUDE=valor['latitude'],
            LONGITUDE=valor['longitude'],
            BAIRRO=valor['bairro'],
            CIDADE=valor['cidade']
        )


def salvar_viagem(numero_viagem, valor):
    # Salve a viagem com o número de viagem atual
    Viagem.objects.create(
        numero_viagem=numero_viagem,
        parada=valor['parada'],
        logradouro=valor['logradouro'],
        bairro=valor['bairro'],
        cidade=valor['cidade'],
        numero=valor['numero'],
        latitude=valor['latitude'],
        longitude=valor['longitude']
    )