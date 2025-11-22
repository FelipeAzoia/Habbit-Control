from django.urls import path
from . import views

urlpatterns = [
    path('alterar_dados/', views.alterar_dados, name='alterar_dados'),
    path('cadastro_garantia/', views.cadastro_garantia, name='cadastro_garantia'),
    path('consultar_garantia/', views.consultar_garantia, name='consultar_garantia'),
    path('api/cliente/update/', views.update_cliente, name='update_cliente'),
]