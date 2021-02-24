from django.urls import path
from .views import UploadFilesView, AdminSiscoFiltrosView, set_data_in_db, CadastroFormView, \
    CadastroListView, CadastroListFormView, RegistrosUnknownView, RegistrosInfosView, delete_register, insert_data_db


urlpatterns = [
    path('admin_sisco/', UploadFilesView.as_view(), name='admin_sisco'),
    path('admin_sisco/set_data/', set_data_in_db, name='set_data'),
    path('admin_sisco/aquisicao/<int:pk>/', AdminSiscoFiltrosView.as_view(), name='filtros_sisco'),
    path('admin_sisco/cadastro/', CadastroFormView.as_view(), name='cadastro_form'),
    path('admin_sisco/cadastro/delete/<int:pk>', delete_register, name='delete_register'),
    path('admin_sisco/cadastro/insert/<int:pk>', insert_data_db, name='insert_data_db'),
    path('admin_sisco/cadastro_list/', CadastroListView.as_view(), name='cadastro_list'),
    path('admin_sisco/cadastro_list/<int:pk>', CadastroListFormView.as_view(), name='cadastro_list_form'),
    path('admin_sisco/registros_unknown/', RegistrosUnknownView.as_view(), name='registros_unknown'),
    path('admin_sisco/registros_infos/', RegistrosInfosView.as_view(), name='registros_infos'),
]
