from django.contrib import admin
from django.contrib.auth import admin as admin_auth
from django.contrib.auth.admin import UserAdmin
from .forms import UserChangeForm, UserCreationForm  # Correção na importação aqui
from .models import CustomUser, Pagamento, CustomPermissionGroup



@admin.register(CustomUser)
class UsersAdmin(admin_auth.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = CustomUser

class PagamentoAdmin(admin.ModelAdmin):
    # Lista de campos para exibição na lista de registros
    list_display = ['id','usuario', 'data_pagamento', 'valido_ate', 'quant_acesso', 'codigo_pagamento']
    # Lista de campos que podem ser editados na lista de registros
    list_editable = ['data_pagamento', 'valido_ate', 'quant_acesso', 'codigo_pagamento']

admin.site.register(Pagamento, PagamentoAdmin)

class CustomUserAdmin(admin_auth.UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff']
    actions = ['disable_users', 'enable_users']

    def disable_users(self, request, queryset):
        # Desativa os usuários selecionados em vez de excluí-los
        queryset.update(is_active=False)

    disable_users.short_description = "Desativar usuários selecionados"

    def enable_users(self, request, queryset):
        # Ativa os usuários selecionados
        queryset.update(is_active=True)

    enable_users.short_description = "Ativar usuários selecionados"

# Verifica se o modelo já está registrado no admin
if not admin.site.is_registered(CustomUser):
    admin.site.register(CustomUser, CustomUserAdmin)


admin.site.register(CustomPermissionGroup)