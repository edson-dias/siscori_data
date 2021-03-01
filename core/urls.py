from django.urls import path, include
from .views import IndexView, ContatoView, AboutView, ExemploView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contato/', ContatoView.as_view(), name='contato'),
    path('sobre/', AboutView.as_view(), name='about'),
    path('exemplos/', ExemploView.as_view(), name='exemplo'),
    path('users/', include('django.contrib.auth.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)