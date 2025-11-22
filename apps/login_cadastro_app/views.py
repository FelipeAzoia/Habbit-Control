from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import ClienteForm, LoginForm
from .models import Cliente

# Create your views here.

def index(request):
    return render(request, 'login_cadastro_app/index.html')

def cadastro_cliente(request):
    """
    Página de cadastro de cliente.
    """
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            nome = form.cleaned_data.get('nome_completo')
            messages.success(request, f'Cadastro realizado com sucesso, {nome}! Faça login.')
            
            return redirect('login') 
        
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, f"{error}")
                    else:
                        label = form.fields[field].label
                        messages.error(request, f"{label}: {error}")
            return render(request, 'login_cadastro_app/cadastro_cliente.html', {'form': form})
    
    else:
        form = ClienteForm()
    
    return render(request, 'login_cadastro_app/cadastro_cliente.html', {'form': form})

# Lógica de Login
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            try:
                # 1. Tenta encontrar o cliente pelo email
                cliente = Cliente.objects.get(email=email)
            except Cliente.DoesNotExist:
                messages.error(request, 'Email ou senha inválidos.')
                return render(request, 'login_cadastro_app/login.html', {'form': form})
            
            # 2. Verifica a senha usando o método check_password do modelo Cliente
            if cliente.check_password(password):
                # Autenticação bem-sucedida (Usando Sessão simples para simular login)
                request.session['cliente_email'] = cliente.email
                messages.success(request, f'Bem-vindo(a), {cliente.nome_completo.split()[0]}!')
                
                # Redireciona para a página interna (alterar_dados, por exemplo)
                return redirect('alterar_dados')
            else:
                messages.error(request, 'Email ou senha inválidos.')
                return render(request, 'login_cadastro_app/login.html', {'form': form})
        
        # Se o formulário não for válido, renderiza com erros
        else:
            return render(request, 'login_cadastro_app/login.html', {'form': form})
    
    else:
        form = LoginForm()
        return render(request, 'login_cadastro_app/login.html', {'form': form})

# Lógica de Logout (Ajustada para usar a session simples)
def logout_view(request):
    if 'cliente_email' in request.session:
        del request.session['cliente_email']
        messages.success(request, 'Logout realizado com sucesso!')
    else:
        messages.info(request, 'Você não estava logado.')
        
    return redirect('index')

def consentimento(request):
    return render(request, 'login_cadastro_app/consentimento.html')