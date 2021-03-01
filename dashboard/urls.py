from django.urls import path
from .views import SearchView, CompView, CotationView, ReportView, SuggestionView, \
    SettingsView, QuantPorMarcaJSONView, ProductDetailsView, ProductDetailsJSONView


urlpatterns = [
    path('dash/', SearchView.as_view(), name='plataforma'),
    path('comp/', CompView.as_view(), name='comparacoes'),
    path('cotacoes/', CotationView.as_view(), name='cotations'),
    path('reports/', ReportView.as_view(), name='reports'),
    path('sugestoes/', SuggestionView.as_view(), name='suggestions'),
    path('configs/', SettingsView.as_view(), name='settings'),
    path('indexdados/', QuantPorMarcaJSONView.as_view(), name='index_dados'),
    path('produtos/<int:pk>', ProductDetailsView.as_view(), name='product_details'),
    path('produtos/product_details_json', ProductDetailsJSONView.as_view(), name='product_details_json')
]