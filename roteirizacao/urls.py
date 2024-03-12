from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import EscolherPlanoView, CustomUserCreationView, atualizar_creditos,  autoriza_criar_rota, buscar_pagamentos, buscar_user, editar_pagamento, editar_user, enviar_email, excluir_pagamento, excluir_user, lista_enderecos, adicionar_endereco, home, lista_pagamento, lista_user, pagamento_form, verificar_saldo

urlpatterns = [
    path('', home, name='home'),
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

]
