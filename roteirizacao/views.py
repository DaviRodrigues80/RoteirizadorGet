from email.headerregistry import Group
from imaplib import _Authenticator
import json
import logging
from django.views.generic import ListView
from multiprocessing import AuthenticationError
from pyexpat.errors import messages
from urllib.request import Request
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext
from django.test import RequestFactory
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, Endereco, Viagem, Pagamento
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, get_user_model
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views import View
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta, timezone
from django.contrib.auth.models import Group, Permission
from django.views.decorators.csrf import csrf_exempt
import requests
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.views.generic import ListView
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Count
from django.db.models import Q
from .forms import ContatoForm, CustomUserCreationForm, PagamentoForm
from django.db.models import F


def home(request):
    # Obtenha o pagamento do usuário atual
    pagamento = None
    if request.user.is_authenticated:
        pagamento = Pagamento.objects.filter(usuario=request.user).order_by('-data_pagamento').first()
        print(pagamento)

    # Renderize o template com o contexto
    return render(request, 'home.html', {'pagamento': pagamento})


def base(request):
    # Obtenha o pagamento do usuário atual
    pagamento = None
    if request.user.is_authenticated:
        pagamento = Pagamento.objects.filter(usuario=request.user).order_by('-data_pagamento').first()

    # Renderize o template com o contexto
    return render(request, 'base.html', {'pagamento': pagamento})

def pagamento_context_processor(request):
    usuario = request.user
    pagamento = None
    if usuario.is_authenticated:
        pagamento = Pagamento.objects.filter(usuario=usuario).order_by('-data_pagamento').first()
    return {'pagamento': pagamento}



logger = logging.getLogger(__name__)


@csrf_exempt
@login_required
@permission_required('roteirizacao_app.add_pagamento', raise_exception=True)
def pagamento_form(request):
    if request.method == 'POST':
        # Se a solicitação for POST, pode ser do formulário HTML ou do JSON
        if request.content_type == 'application/json':
            # Obter os dados JSON do corpo da solicitação
            json_data = json.loads(request.body)
            
            # Acessar os dados individuais
            usuario_id = json_data.get('usuario_id')
            data_pagamento = json_data.get('data_pagamento')
            codigo_pagamento = json_data.get('codigo_pagamento')
        else:
            # Se a solicitação for do formulário HTML
            form = PagamentoForm(request.POST)
            if form.is_valid():
                # Se o formulário for válido, salvar os dados do formulário
                pagamento = form.save(commit=False)
                pagamento.valido_ate = pagamento.data_pagamento + timedelta(days=30)
                pagamento.quant_acesso = 30  # Ou o valor que desejar
                pagamento.save()
                return redirect('home')  # Redirecionar para a mesma página após o envio do formulário
            else:
                # Se o formulário não for válido, retornar uma resposta de erro
                return JsonResponse({'error': 'Formulário inválido.'}, status=400)

        # Criar uma instância do modelo Pagamento com os dados fornecidos
        pagamento = Pagamento.objects.create(
            usuario_id=usuario_id,
            data_pagamento=data_pagamento,
            valido_ate=timezone.now() + timedelta(days=30),  # Exemplo de data de validade
            quant_acesso=30,  # Exemplo de quantidade de acesso inicial
            codigo_pagamento=codigo_pagamento
        )
        
        # Salvar o objeto Pagamento no banco de dados
        pagamento.save()

        # Retornar uma resposta JSON de sucesso
        return JsonResponse({'success': True})

    elif request.method == 'GET':
        # Se a solicitação for GET, renderize o template do formulário de pagamento
        form = PagamentoForm()
        return render(request, 'pagamento.html', {'form': form})
    else:
        # Se o método de solicitação não for permitido, retorne um erro 405
        return JsonResponse({'error': 'Método não permitido.'}, status=405)
    

## CLASS CUSTOMLOGIN
class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('adicionar')

class CustomUserCreationView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')  # Redireciona para a página de login após o cadastro bem-sucedido

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

def home(request):
    return render(request, 'home.html', {'user': request.user})

def lista_enderecos(request):
    enderecos = Endereco.objects.all()
    return render(request, 'lista_enderecos.html', {'enderecos': enderecos})

@login_required
def adicionar_endereco(request):
    
    return render(request, 'adicionar_enderecos.html')

@login_required
def lista_pagamento(request):
    filtro = request.GET.get('filtro')

    # Filtra os pagamentos com base no filtro
    if filtro:
        pagamentos = Pagamento.objects.filter(
            Q(id__icontains=filtro) |
            Q(usuario__username__icontains=filtro) |
            Q(codigo_pagamento__icontains=filtro)
        )
    else:
        pagamentos = Pagamento.objects.all()

    return render(request, 'lista_pagamento.html', {'pagamentos': pagamentos})

def processar_pagamento(request):
    if request.method == 'POST':
        # Capturar os dados do POST
        usuario_id = request.POST.get('usuario_id')
        data_pagamento = request.POST.get('data_pagamento')
        codigo_pagamento = request.POST.get('codigo_pagamento')

        # Validar os dados (verificar se todos os campos foram enviados)
        if not usuario_id or not data_pagamento or not codigo_pagamento:
            return JsonResponse({'status': 'error', 'message': 'Todos os campos são obrigatórios.'})

        # Salvar os dados no banco de dados
        pagamento = Pagamento(usuario_id=usuario_id, data_pagamento=data_pagamento, codigo_pagamento=codigo_pagamento)
        pagamento.save()

        # Retornar uma resposta de sucesso
        return JsonResponse({'status': 'success', 'message': 'Pagamento processado com sucesso.'})
    else:
        # Se a requisição não for do tipo POST, retornar um erro
        return JsonResponse({'status': 'error', 'message': 'Método não permitido.'})

@login_required
def editar_pagamento(request, pagamento_id):
    # Busca o pagamento correspondente ao ID fornecido
    pagamento = get_object_or_404(Pagamento, pk=pagamento_id)
    
    # Verifica se o formulário foi submetido
    if request.method == 'POST':
        form = PagamentoForm(request.POST, instance=pagamento)
        if form.is_valid():
            form.save()
            return redirect('lista_pagamento')
    else:
        # Inicializa o formulário com os dados do pagamento
        form = PagamentoForm(instance=pagamento)
    
    return render(request, 'editar_pagamento.html', {'form': form, 'pagamento': pagamento})

@login_required
def excluir_pagamento(request, pagamento_id):
    # Busca o pagamento correspondente ao ID fornecido
    pagamento = get_object_or_404(Pagamento, pk=pagamento_id)
    
    # Verifica se o formulário foi submetido
    if request.method == 'POST':
        pagamento.delete()
        return redirect('lista_pagamento')
    else:
        return render(request, 'confirmar_exclusao_pagamento.html', {'pagamento': pagamento})

@login_required
def buscar_pagamentos(request):
    if request.method == 'GET':
        pagamento_id = request.GET.get('pagamento_id')
        if pagamento_id:
            try:
                # Busca o pagamento com base no ID fornecido
                pagamento = get_object_or_404(Pagamento, pk=pagamento_id)
                # Renderiza a tabela de pagamentos em HTML
                pagamentos_html = render_to_string('pagamentos_table.html', {'pagamentos': [pagamento]})
                return JsonResponse({'editar_pagamentos.html': pagamentos_html})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'ID do pagamento não fornecido na solicitação'}, status=400)
    else:
        return JsonResponse({'error': 'Método de solicitação não suportado'}, status=405)

@login_required
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


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                
                return redirect('home')
            else:
                print("Usuário não autenticado. Verifique as credenciais.")
        else:
            print("Formulário inválido.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Autenticar o usuário após o cadastro
            authenticated_user = authenticate(request, username=user.username, password=form.cleaned_data['password1'])
            if authenticated_user is not None:
                login(request, authenticated_user)
            
            # Adicione uma mensagem de sucesso
            messages.success(request, 'Cadastro realizado com sucesso. Faça login para continuar.')

            # Redirecione para a tela de login
            return redirect('processar_pagamento')  # ou qualquer URL desejada
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})



# Configurações para Processamento de pagamento - Inicio
  
@method_decorator(login_required, name='dispatch')
class EscolherPlanoView(View):
    template_name = 'escolher_plano.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if not request.user.is_authenticated:
            messages.error(request, 'Você precisa fazer login antes de acessar esta página.')
            return render(request, 'login_cadastro_opcao.html')
            # Redirecione para a página onde você exibe as opções de login ou cadastro
        else:
            form = PagamentoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')
            else:
                return render(request, 'pagamento.html', {'form': form})
    
# Processamento de pagamento - Fim

# Autoriza Criar Rota
@login_required
#@method_decorator(login_required, name='dispatch')
#@permission_required('roteirizacao_app.criar_rota', raise_exception=True)
def autoriza_criar_rota(request):
    try:
        print("Entrou na função autoriza_criar_rota")  # Debug: Verifica se a função foi chamada

        usuario = request.user
        print(f'Usuário autenticado: {usuario.username}')  # Debug: Verifica o usuário autenticado

        pagamento = Pagamento.objects.filter(usuario=usuario).order_by('-data_pagamento').first()
        if pagamento:
            print(f'Pagamento encontrado: {pagamento.id}, Data: {pagamento.data_pagamento}, Valido até: {pagamento.valido_ate}, Quantidade de acessos: {pagamento.quant_acesso}')
        else:
            print('Nenhum pagamento encontrado para este usuário')  # Debug: Verifica se o pagamento foi encontrado

        if pagamento and pagamento.valido_ate >= timezone.now().date() and pagamento.quant_acesso > 0:
            print('Acesso concedido para criar rota')  # Debug: Verifica se o acesso foi concedido
            return render(request, 'adicionar_enderecos.html', {'mensagem': 'Acesso concedido para criar rota.','pagamento': pagamento})
        else:
            print('Permissão negada para criar rota')  # Debug: Verifica se a permissão foi negada
            return render(request, 'escolher_plano.html', {'mensagem': 'Você não tem permissão para criar rota. Faça um pagamento ou recarregue seus créditos.'})
    except Pagamento.DoesNotExist:
        print('Nenhum pagamento encontrado para este usuário')  # Debug: Verifica se o pagamento foi encontrado
        return render(request, 'escolher_plano.html', {'mensagem': 'Você não tem permissão para criar rota. Faça um pagamento para continuar.'})
    except Exception as e:
        print(f'Erro ao verificar permissão para criar rota: {e}')  # Debug: Verifica se ocorreu um erro inesperado
        raise PermissionDenied('Erro ao verificar permissão para criar rota: {}'.format(str(e)))


# Requisição para gerar PIX


# Listar e editar pagamento
@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('roteirizacao_app.view_pagamento', raise_exception=True), name='dispatch')
class ListaPagamentoView(ListView):
    model = Pagamento
    template_name = 'lista_pagamento.html'  # Nome do seu template
    context_object_name = 'pagamentos'


### Enviar Email para contato
def enviar_email(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            mensagem = form.cleaned_data['mensagem']
            # Envie o email
            send_mail(
                'Assunto do Email',
                mensagem,
                email,
                ['getexpresstransportes@gmail.com'],
                fail_silently=False,
            )
            # Redirecione para uma página de sucesso
            return render(request, 'sucesso.html')
    else:
        form = ContatoForm()
    return render(request, 'contato.html', {'form': form})

## Def verificar saldo -  inicio
def verificar_saldo(request):
    usuario = request.user
    pagamento = Pagamento.objects.filter(usuario_id=usuario.id).last()
    saldo_suficiente = pagamento and pagamento.valido_ate >= timezone.now()
    if saldo_suficiente:
        # Descontar 1 do campo quant_acesso
        if pagamento.quant_acesso > 0:
            pagamento.quant_acesso -= 1
            pagamento.save()
        else:
            saldo_suficiente = False  # Não há crédito suficiente, pois quant_acesso é zero
    return JsonResponse({'saldo_suficiente': saldo_suficiente})

## Def verificar saldo -  fim


def atualizar_creditos(request):
    if request.method == 'POST':
        # Sua lógica para atualizar os créditos do usuário vai aqui...
        usuario = request.user
        pagamento = Pagamento.objects.filter(usuario_id=usuario.id).last()
        if pagamento:
            pagamento.quant_acesso -= 1
            pagamento.save()
        else:
            return redirect('escolher_plano')
        
        return JsonResponse({'message': 'Créditos do usuário atualizados com sucesso!'})
    else:
        return JsonResponse({'error': 'Método não permitido'}, status=405)