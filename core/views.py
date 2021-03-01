from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class ContatoView(TemplateView):
    template_name = 'contato.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class ExemploView(TemplateView):
    template_name = 'exemplos.html'




'''   

class AdminRegisterView(LoginRequiredMixin, FormView):
    template_name = 'background_sisco/admin_upload.html'
    form_class = GetSiscoriFilesForm
    success_url = reverse_lazy('admin_sisco/')

    def get_context_data(self, **kwargs):
        context = super(AdminRegisterView, self).get_context_data(**kwargs)
        arq1 = self.request.FILES.get('arquivo1')
        teste = SiscoriData(files=arq1)
        teste.save()
        return context
        
import urllib.request 
class PlataformaView(LoginRequiredMixin, TemplateView):
    template_name = 'dash/dash_index.html'
    login_url = '/users/login/'

    def _get_cotation_page(self):
        site = 'https://valor.globo.com/valor-data/'
        self.page = urllib.request.urlopen(site)
        return self.page

    def _get_bs4_page(self):
        self.soup = BeautifulSoup(self._get_cotation_page(), 'html5lib')
        return self.soup

    def _get_cotation(self):
        self.list_cotation = self._get_bs4_page().find('div', attrs={'class': 'cell auto data-cotacao__ticker_quote'})
        return self.list_cotation

    def get_context_data(self, **kwargs):
        context = super(PlataformaView, self).get_context_data(**kwargs)
        context['dolar'] = self._get_cotation().text
        return context

'''