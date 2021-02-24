from django.views.generic import TemplateView, ListView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from bs4 import BeautifulSoup
from .models import Infos, ValoresMensais
from chartjs.views.lines import BaseLineChartView
from datetime import date


def get_query_convert_to_dict(search):
    data = {}
    cluster_marca = []

    query = ValoresMensais.objects.filter(search).order_by('infos_prod__marca')

    if query.first():
        for itens in query:
            if not cluster_marca:
                cluster_marca.append((itens.mes, itens.ano, itens.valor, itens.quant,
                                      itens.infos_prod.nome_prod, itens.infos_prod.marca))
            else:
                if itens.infos_prod.marca == cluster_marca[-1][5]:
                    cluster_marca.append((itens.mes, itens.ano, itens.valor, itens.quant,
                                          itens.infos_prod.nome_prod, itens.infos_prod.marca))
                else:
                    data[cluster_marca[-1][5]] = cluster_marca
                    cluster_marca = [(itens.mes, itens.ano, itens.valor, itens.quant,
                                      itens.infos_prod.nome_prod, itens.infos_prod.marca)]

        data[cluster_marca[-1][5]] = cluster_marca

    return data


def get_quant_from_dict(data_dict):
    data = []
    months = [0] * 12

    for values in data_dict.values():
        for itens in values:
            if itens[0] == 1:
                months[0] = months[0] + itens[3]
            elif itens[0] == 2:
                months[1] = months[1] + itens[3]
            elif itens[0] == 3:
                months[2] = months[2] + itens[3]
            elif itens[0] == 4:
                months[3] = months[3] + itens[3]
            elif itens[0] == 5:
                months[4] = months[4] + itens[3]
            elif itens[0] == 6:
                months[5] = months[5] + itens[3]
            elif itens[0] == 7:
                months[6] = months[6] + itens[3]
            elif itens[0] == 8:
                months[7] = months[7] + itens[3]
            elif itens[0] == 9:
                months[8] = months[8] + itens[3]
            elif itens[0] == 10:
                months[9] = months[9] + itens[3]
            elif itens[0] == 11:
                months[10] = months[10] + itens[3]
            elif itens[0] == 12:
                months[11] = months[11] + itens[3]
        data.append(months)
        months = [0] * 12
    return data


class IndexView(TemplateView):
    template_name = 'index.html'


class ContatoView(TemplateView):
    template_name = 'contato.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class ExemploView(TemplateView):
    template_name = 'exemplos.html'


class SearchView(LoginRequiredMixin, ListView):
    model = Infos
    template_name = 'dashboard/dash_index.html'
    context_object_name = 'all_search_results'

    months = {
        1: 'Janeiro',
        2: 'Fevereiro',
        3: 'Março',
        4: 'Abril',
        5: 'Maio',
        6: 'Junho',
        7: 'Julho',
        8: 'Agosto',
        9: 'Setembro',
        10: 'Outubro',
        11: 'Novembro',
        12: 'Dezembro'
    }

    years = {}
    i_year = 2019
    delta_year = date.today().year - i_year
    i = delta_year
    while i >= 0:
        years[i_year + i] = i_year + i
        i -= 1
# TODO: Melhorar a apresentação na tabela do campo "Valor"

    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        # TODO: Ajustar as declarações abaixo no formato de um dict = {}
        search = self.request.GET.get('search')
        brands = self.request.GET.get('brands')
        i_month = self.request.GET.get('i_month')
        f_month = self.request.GET.get('f_month')
        year_options = self.request.GET.get('year_options')

        self.request.session['search'] = search
        self.request.session['brands'] = brands
        self.request.session['i_month'] = i_month
        self.request.session['f_month'] = f_month
        self.request.session['year_options'] = year_options

        if search:
            filter_q = (Q(infos_prod__nome_prod__icontains=search) | Q(infos_prod__cod_marca__icontains=search))

            if year_options:
                filter_q.add(Q(ano__icontains=year_options), Q.AND)
            if i_month and f_month:
                filter_q.add(Q(mes__gte=i_month), Q.AND)
                filter_q.add(Q(mes__lte=f_month), Q.AND)
            if brands:
                filter_q.add(Q(infos_prod__marca__icontains=brands), Q.AND)

            postresult = ValoresMensais.objects.filter(filter_q).order_by('mes')
            result = postresult
        else:
            result = None
        return result

    def get_context_data(self, **kwargs):

        context = super(SearchView, self).get_context_data(**kwargs)
        search = self.request.GET.get('search')
        context['search'] = search
        context['years'] = self.years
        context['months'] = self.months
        return context


class CompView(ListView):
    template_name = 'dashboard/comparacoes.html'
    model = Infos

    def get_context_data(self, **kwargs):
        context = super(CompView, self).get_context_data(**kwargs)
        return context


class QuantPorMarcaJSONView(BaseLineChartView):
    # TODO: Função que verifica o intervalo max e min de meses dos dados e aplica nas labels
    def get_labels(self):
        labels = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro',
                  'Novembro', 'Dezembro']
        return labels

    def get_providers(self):
        search = self.request.session.get('search')
        brands = self.request.session.get('brands')
        i_month = self.request.session.get('i_month')
        f_month = self.request.session.get('f_month')
        year_options = self.request.session.get('year_options')

        if search:
            filter_q = (Q(infos_prod__nome_prod__icontains=search) | Q(infos_prod__cod_marca__icontains=search))

            if year_options:
                filter_q.add(Q(ano__icontains=year_options), Q.AND)
            if i_month and f_month:
                filter_q.add(Q(mes__gte=i_month), Q.AND)
                filter_q.add(Q(mes__lte=f_month), Q.AND)
            if brands:
                filter_q.add(Q(infos_prod__marca__icontains=brands), Q.AND)

            datasets = []
            data_chart = get_query_convert_to_dict(filter_q)
            [datasets.append(keys) for keys in data_chart.keys()]
            return datasets
        else:
            return ''

    def get_data(self):
        search = self.request.session.get('search')
        brands = self.request.session.get('brands')
        i_month = self.request.session.get('i_month')
        f_month = self.request.session.get('f_month')
        year_options = self.request.session.get('year_options')

        if search:
            filter_q = (Q(infos_prod__nome_prod__icontains=search) | Q(infos_prod__cod_marca__icontains=search))

            if year_options:
                filter_q.add(Q(ano__icontains=year_options), Q.AND)
            if i_month and f_month:
                filter_q.add(Q(mes__gte=i_month), Q.AND)
                filter_q.add(Q(mes__lte=f_month), Q.AND)
            if brands:
                filter_q.add(Q(infos_prod__marca__icontains=brands), Q.AND)

            data_chart = get_query_convert_to_dict(filter_q)
            data = get_quant_from_dict(data_chart)
            return data
        else:
            return ''


class DadosJSONView(BaseLineChartView):

    def get_labels(self):
        pass

    def get_providers(self):
        """Retorna os nomes dos datasets."""
        datasets = [
            "Programação para Leigos",
            "Teste"
        ]
        return datasets

    def get_data(self):
        """
        Retorna 6 datasets para plotar o gráfico.

        Cada linha representa um dataset.
        Cada coluna representa um label.

        A quantidade de dados precisa ser igual aos datasets/labels

        12 labels, então 12 colunas.
        6 datasets, então 6 linhas.
        """

        data = []
        return data


class CotationView(ListView):
    template_name = 'dashboard/cotations.html'
    model = Infos


class SettingsView(ListView):
    template_name = 'dashboard/settings.html'
    model = Infos


class ReportView(ListView):
    template_name = 'dashboard/reports.html'
    model = Infos


class SuggestionView(ListView):
    template_name = 'dashboard/suggestions.html'
    model = Infos


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