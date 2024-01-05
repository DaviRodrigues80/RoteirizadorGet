from django import forms
from .models import Endereco, Viagem

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