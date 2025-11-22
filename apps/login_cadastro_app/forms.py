from django import forms
from .models import Cliente
from django.contrib.auth.hashers import make_password

class ClienteForm(forms.ModelForm):
    # Sobrescreve o campo Senha para usar o Widget de Senha (oculta o texto)
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha'}),
        max_length=100,
        required=True
    )
    
    class Meta:
        model = Cliente
        fields = ['nome_completo', 'idade', 'cpf', 'email', 'password', 'cidade', 'pais', 'profissao', 'lgpd']
        
        widgets = {
            'nome_completo': forms.TextInput(attrs={'placeholder': 'Seu nome completo'}),
            'cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
            'email': forms.EmailInput(attrs={'placeholder': 'seu.email@exemplo.com'}),
        }

    # O método save() do modelo Cliente já faz o hasheamento, então aqui apenas garante que o valor seja passado
    def clean_password(self):
        return self.cleaned_data.get('password')
    
    # Sobrescreve o save para garantir que a senha seja tratada (embora o modelo Cliente já faça isso)
    def save(self, commit=True):
        cliente = super().save(commit=False)
        if commit:
            cliente.save()
        return cliente


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Seu email de cadastro'}),
        required=True
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha'}),
        required=True
    )