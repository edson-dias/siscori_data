from .models import SiscoriFiles
from django import forms
from core.models import Infos


class GetSiscoriFilesForm(forms.ModelForm):
    class Meta:
        model = SiscoriFiles
        fields = ('files',)


class CadastroListForm(forms.ModelForm):
    keywords = forms.CharField(label='Chaves', max_length=70, required=True,)

    class Meta:
        model = Infos
        fields = ('nome_prod', 'marca', 'cod_marca', 'descricao', )
