from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from apps.login_cadastro_app.models import Cliente # Removido Revendedor

# Create your views here.

def alterar_dados(request):
	"""Render the dashboard 'Alterar Dados' page with client data."""
	try:
		# Tenta buscar o cliente pelo email do usuário logado
		# Se não estiver autenticado, usa um cliente de exemplo (para desenvolvimento)
		if request.user.is_authenticated:
			cliente = Cliente.objects.filter(email=request.user.email).first()
		else:
			# Para desenvolvimento: busca o primeiro cliente
			cliente = Cliente.objects.first()
		
		context = {'cliente': cliente}
		return render(request, 'pagina_interna/alterar_dados_cliente.html', context)
	except Exception as e:
		print(f"Erro ao buscar cliente: {str(e)}")
		return render(request, 'pagina_interna/alterar_dados_cliente.html', {'cliente': None})


def cadastro_garantia(request):
	"""Render the 'Cadastro de Garantia' page."""
	# templates were renamed to include the `_cliente` suffix
	return render(request, 'pagina_interna/cadastro_garantia_cliente.html')


def consultar_garantia(request):
	"""Render the 'Consultar Garantia' page."""
	# templates were renamed to include the `_cliente` suffix
	return render(request, 'pagina_interna/consultar_garantia_cliente.html')


# As views administrativas a seguir foram removidas ou simplificadas,
# pois dependiam de modelos ou templates inexistentes.

# Removidas as views 'validar_garantias_adm', 'cadastrar_produtos_adm', 'clientes_adm', 
# 'consultar_garantias_adm', 'relatorios_adm', e 'revenda_adm', pois elas se
# referem a funcionalidades administrativas que você indicou ter removido.


# NOTA: Manter apenas a view 'revenda_adm' (renomeada abaixo para simplicidade)
# causará erro se o template 'pagina_interna/revenda_adm.html' não existir.
# Para manter a compatibilidade e não quebrar outras URLs que possam referenciar
# essas views, vou apenas COMENTAR as que dependem de Revendedor/Admin:

# def validar_garantias_adm(request):
# 	return render(request, 'pagina_interna/validar_garantia_adm.html')

# def cadastrar_produtos_adm(request):
# 	return render(request, 'pagina_interna/cadastrar_produtos_adm.html')

# ... (outras views admin removidas/comentadas) ...

# A view 'revenda_adm' e todas as outras views _adm foram removidas
# pois dependem do modelo Revendedor e dos templates admin que você apagou.
# Se você precisar da lógica de revendedor novamente, deve recriar o modelo Revendedor.

def revenda_adm(request):
	# Esta view foi modificada para retornar um 404 ou uma página vazia,
	# já que depende do modelo Revendedor e templates _adm que foram removidos.
	# Retornando uma página simples para evitar o crash de importação.
	return render(request, 'pagina_interna/home.html') 


@require_POST
def update_cliente(request):
    """Handle AJAX requests to update client data."""
    try:
        data = json.loads(request.body)
        field = data.get('field')
        value = data.get('value')
        
        # Validação básica
        if not field or value is None: # value pode ser string vazia, mas não None
            return JsonResponse({'success': False, 'error': 'Campo ou valor inválido'}, status=400)
        
        # 1. Busca o Cliente
        if request.user.is_authenticated:
            cliente = Cliente.objects.filter(email=request.user.email).first()
        else:
            # Fallback para dev
            cliente = Cliente.objects.first()
        
        if not cliente:
            return JsonResponse({'success': False, 'error': 'Cliente não encontrado'}, status=404)
        
        # 2. LISTA DE CAMPOS PERMITIDOS (Atualizada para os novos campos)
        # Chave = O que vem do JavaScript (edit_profile.js)
        # Valor = Nome da coluna no seu models.py
        field_map = {
            'nome_completo': 'nome_completo',
            'idade': 'idade',
            'cpf': 'cpf',
            'email': 'email',
            'password': 'password', # O JS manda 'password', o model tem 'password'
            'cidade': 'cidade',
            'pais': 'pais',
            'profissao': 'profissao'
        }

        # Verifica se o campo enviado é permitido
        if field not in field_map:
            print(f"[ERRO] Tentativa de editar campo não permitido: {field}")
            return JsonResponse({'success': False, 'error': f'Campo {field} não permitido'}, status=400)
        
        model_field = field_map[field]

        # 3. Lógica Especial para Senha
        if model_field == 'password':
            if not value:
                return JsonResponse({'success': False, 'error': 'A senha não pode ser vazia'}, status=400)
            # Nota: Como seu model tem um override no método save(), 
            # basta atribuir o valor 'cru' aqui que o save() fará o hash.
            cliente.password = value
        else:
            # Atribuição genérica para os outros campos
            setattr(cliente, model_field, value)

        # 4. Salvar
        cliente.save()
        
        print(f"[SUCESSO] Cliente {cliente.id} atualizou {model_field}.")
        return JsonResponse({'success': True, 'message': 'Dados atualizados com sucesso'})
    
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'JSON inválido'}, status=400)
    except Exception as e:
        print(f"[ERRO CRÍTICO] {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)