from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import Endereco, Pagamento, Viagem, CustomUser



# Tabela Endereco
class EnderecoForm(forms.ModelForm):
    id_temporario = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Endereco
        fields = ['cep', 'logradouro', 'latitude','longitude', 'bairro', 'cidade', 'numero']



# Tabela Viagem
class ViagemForm(forms.ModelForm):
    

    class Meta:
        model= Viagem
        fields =  ['numero_viagem', 'parada', 'lougradouro', 'bairro', 'cidade', 'numero', 'latitude', 'longitude']

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')


class ContatoForm(forms.Form):
    email = forms.EmailField(label='E-mail')
    mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea)

class PagamentoForm(forms.ModelForm):
    usuario = forms.ModelChoiceField(queryset=CustomUser.objects.all())  # Use o modelo CustomUser

    class Meta:
        model = Pagamento
        fields = ['id','usuario', 'codigo_pagamento' ,'data_pagamento', 'valido_ate', 'quant_acesso']

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['password', 'is_superuser', 'username', 'first_name', 'last_name', 'is_staff', 'cargo', 'email', 'is_active']
