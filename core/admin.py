from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUsuarioChangeForm, CustomUsuarioCreateForm
from .models import Infos, ValoresMensais, CustomUsuario


@admin.register(CustomUsuario)
class CustomUsuarioAdmin(UserAdmin):
    add_form = CustomUsuarioCreateForm
    form = CustomUsuarioChangeForm
    model = CustomUsuario
    list_display = ('first_name', 'last_name', 'email', 'fone', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'fone')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(ValoresMensais)
class ValoresMensaisAdmin(admin.ModelAdmin):
    list_display = ('mes', 'ano', 'quant', 'valor', 'get_marca', 'infos_prod')

    def get_marca(self, obj):
        return obj.infos_prod.marca
    get_marca.short_description = 'Marca'
    get_marca.admin_order_field = 'infos_prod.marca'


@admin.register(Infos)
class InfosAdmin(admin.ModelAdmin):
    list_display = ('nome_prod', 'marca', 'cod_marca', 'descricao', 'ncm', 'porto', 'pa', 'po')

