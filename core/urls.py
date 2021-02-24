from django.urls import path, include
from .views import IndexView, ContatoView, AboutView, ExemploView, SearchView, CompView, CotationView, \
    ReportView, SuggestionView, SettingsView, QuantPorMarcaJSONView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contato/', ContatoView.as_view(), name='contato'),
    path('sobre/', AboutView.as_view(), name='about'),
    path('exemplos/', ExemploView.as_view(), name='exemplo'),
    path('users/', include('django.contrib.auth.urls')),
    path('dash/', SearchView.as_view(), name='plataforma'),
    path('comp/', CompView.as_view(), name='comparacoes'),
    path('cotacoes/', CotationView.as_view(), name='cotations'),
    path('reports/', ReportView.as_view(), name='reports'),
    path('sugestoes/', SuggestionView.as_view(), name='suggestions'),
    path('configs/', SettingsView.as_view(), name='settings'),
    path('indexdados/', QuantPorMarcaJSONView.as_view(), name='index_dados'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)