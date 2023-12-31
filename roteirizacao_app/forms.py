from django import forms
from .models import Endereco

# Adicione um campo temporário para o ID
class EnderecoForm(forms.ModelForm):
    id_temporario = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Endereco
        fields = ['cep', 'rua', 'latitude','longitude', 'bairro', 'cidade', 'numero']
