from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template import RequestContext
from .models import Endereco
from .forms import EnderecoForm

def lista_enderecos(request):
    enderecos = Endereco.objects.all()
    return render(request, 'roteirizacao_app/lista_enderecos.html', {'enderecos': enderecos})

def buscar_cep(request):
    if request.method == 'POST':
        cep = request.POST.get('cep')
        numero = request.POST.get('numero')

        # Verifica se o CEP e número já existem no banco de dados
        endereco = Endereco.objects.filter(cep=cep, numero=numero).first()

        if endereco:
            data = {
                'rua': endereco.rua,
                'numero':endereco.numero,
                'latitude': endereco.latitude,
                'longitude': endereco.longitude,
                'bairro': endereco.bairro,
                'cidade': endereco.cidade,
            }
            return JsonResponse(data)
        else:
            # Se o endereço não existir no banco, faz a requisição à API VIA CEP
            url = f'https://viacep.com.br/ws/{cep}/json/'
            response = RequestContext.get(url)
            data = response.json()

            if 'erro' not in data:
                # Se a API retornar dados válidos, preenche os campos do formulário
                data_to_return = {
                    'rua': data.get('logradouro', ''),
                    'numero':data.get('numero', ''),
                    'latitude':data.get('latitude', ''),
                    'longitude':data.get('longitude', ''),
                    'bairro': data.get('bairro', ''),
                    'cidade': data.get('localidade', ''),
                }
                return JsonResponse(data_to_return)

    return JsonResponse({'error': 'Método não permitido'})

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

    return render(request, 'roteirizacao_app/adicionar_enderecos.html', {'form': form})

def lista_enderecos_temporarios(request):
    enderecos_temporarios = request.session.get('enderecos_temporarios', [])
    return render(request, 'roteirizacao_app/lista_enderecos.html', {'enderecos_temporarios': enderecos_temporarios})