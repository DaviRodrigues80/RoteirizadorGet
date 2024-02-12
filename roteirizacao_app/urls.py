from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import EscolherPlanoView, CustomUserCreationView,  autoriza_criar_rota, buscar_pagamentos, editar_pagamento, enviar_email, excluir_pagamento, lista_enderecos, adicionar_endereco, home, lista_pagamento, pagamento_form, verificar_saldo

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
    

]
