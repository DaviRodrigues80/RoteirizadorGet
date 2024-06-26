from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import EscolherPlanoView, CustomUserCreationView, atualizar_creditos, atualizar_senha,  autoriza_criar_rota, base2, buscar_pagamentos, buscar_user, contato, editar_pagamento, editar_user, enviar_email, excluir_pagamento, excluir_user, gerar_arquivo_gpx_view, lista_enderecos, adicionar_endereco, home, lista_pagamento, lista_user, pagamento_form, recuperar_senha, recursos, sobre, verificar_saldo
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('base2/', base2, name='base2'),
    path('sobre/', sobre, name='sobre'),
    path('recursos/', recursos, name='recursos'),
    path('contato/', contato, name='contato'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', CustomUserCreationView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('lista_enderecos', lista_enderecos, name='lista_enderecos'),
    path('adicionar/', adicionar_endereco, name='adicionar'),
    path('escolher_plano/', EscolherPlanoView.as_view(), name='escolher_plano'),
    path('enviar_email/', enviar_email, name='enviar_email'),
    path('verificar_saldo/', verificar_saldo, name='verificar_saldo'),
    path('lista_pagamento/', lista_pagamento, name='lista_pagamento'),
    path('pagamento/', pagamento_form, name='pagamento'),
    path('autoriza_criar_rota/', autoriza_criar_rota, name='autoriza_criar_rota'),
    path('buscar_pagamentos/', buscar_pagamentos, name='buscar_pagamentos'),
    path('editar_pagamento/<int:pagamento_id>/', editar_pagamento, name='editar_pagamento'),
    path('excluir_pagamento/<int:pagamento_id>/', excluir_pagamento, name='excluir_pagamento'),
    path('atualizar_creditos/', atualizar_creditos, name='atualizar_creditos'),
    path('lista_user/', lista_user, name='lista_user'),
    path('buscar_user/', buscar_user, name='buscar_user'),
    path('editar_user/<int:user_id>/', editar_user, name='editar_user'),
    path('excluir_user/<int:user_id>/', excluir_user, name='excluir_user'),
    path('recuperar-senha/', recuperar_senha, name='recuperar_senha'),
    path('atualizar-senha/', atualizar_senha, name='atualizar_senha'),
    path('gerar_arquivo_gpx/', gerar_arquivo_gpx_view, name='gerar_arquivo_gpx'),

]
