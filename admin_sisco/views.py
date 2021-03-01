from django.views.generic import TemplateView, CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse_lazy

from core.src import utils
from core.models import Infos, KeywordSiscori

from .forms import GetSiscoriFilesForm, CadastroListForm
from .models import SiscoriFiles, SiscoriHistory, NcmSiscoriFilter, CountrySiscoriFilter, SiscoriUnknownData, \
    validate_and_set_new_infos, _set_data


def delete_register(request, pk):
    if request.method == 'POST':
        deleted_item = SiscoriUnknownData.objects.get(pk=pk)
        deleted_item.delete()
    return redirect('cadastro_form')


def insert_data_db(request, pk):
    if request.method == 'POST':
        brand = request.POST.get('marca')
        keyword = request.POST.get('keyword')
        cod_prod = request.POST.get('cod_prod')
        prod_name = request.POST.get('prod_name')
        description = request.POST.get('descricao_prod')
        query = SiscoriUnknownData.objects.get(pk=pk)
        validate_and_set_new_infos(new_query=query, nome_prod=prod_name, marca=brand, cod_marca=cod_prod,
                                   descricao=description, chaves=keyword)
    return redirect('cadastro_form')


def set_data_in_db(request):
    # TODO: Implementar opções de novos filtros.

    if request.method == 'POST':
        ncm_filter = request.POST.get('ncm')
        countries_filter = request.POST.get('country')

        ncm_filter = utils.convert_string_to_list(ncm_filter)
        countries_filter = utils.convert_string_to_list(countries_filter)

        keys_database = KeywordSiscori.objects.all()
        files = SiscoriFiles.objects.all()

        for plan_csv in files:
            records = SiscoriHistory.objects.filter(files=plan_csv.files)
            if not records:
                _set_data(plan_csv, ncm_filter, countries_filter, keys_database)

            else:
                recorded_filters = [[], []]
                actual_filter = [[], []]
                used_filters = [[], []]
                new_filter = [[], []]

                actual_filter[0] = ncm_filter
                actual_filter[1] = countries_filter

                for itens in records:
                    used_filters[0] = utils.convert_string_to_list(itens.n_filters)
                    used_filters[1] = utils.convert_string_to_list(itens.c_filters)
                    recorded_filters[0] = recorded_filters[0] + used_filters[0]
                    recorded_filters[1] = recorded_filters[1] + used_filters[1]

                [new_filter[0].append(n_filter) for n_filter in recorded_filters[0] if n_filter not in actual_filter[0]]
                [new_filter[1].append(c_filter) for c_filter in recorded_filters[1] if c_filter not in actual_filter[1]]

                if not new_filter[0] and not new_filter[1]:
                    pass

                else:
                    if not new_filter[0]:
                        new_filter[0] = ncm_filter
                    elif not new_filter[1]:
                        new_filter[1] = countries_filter

                    _set_data(plan_csv, new_filter[0], new_filter[1], keys_database)

        # Siscori plan index: ANOMES=0 /NCM=1 /ORIGIN_COUNTRY=2 /ACQUISITION_COUNTRY=3 DESCRIPTION=4 /VALUE=5 /QUANTITY=6 /HARBOR=7
        return redirect('admin_sisco')


class UploadFilesView(LoginRequiredMixin, CreateView):
    template_name = 'admin_upload.html'
    model = SiscoriFiles
    form_class = GetSiscoriFilesForm
    success_url = reverse_lazy('admin_sisco')

    def get_context_data(self, **kwargs):
        context = super(UploadFilesView, self).get_context_data(**kwargs)

        query = SiscoriFiles.objects.all()
        ncm_filters = NcmSiscoriFilter.objects.all()
        countries_filter = CountrySiscoriFilter.objects.all()

        context['country'] = countries_filter
        context['ncm'] = ncm_filters
        context['query'] = query
        return context


class CadastroFormView(LoginRequiredMixin, TemplateView):
    template_name = 'cadastro_form.html'
    success_url = reverse_lazy('cadastro_form')

    def get_context_data(self, **kwargs):
        context = super(CadastroFormView, self).get_context_data(**kwargs)
        page = self.request.GET.get('page')
        query = SiscoriUnknownData.objects.all().order_by('month')
        paginator = Paginator(query, 1)
        posts = paginator.get_page(page)
        context['posts'] = posts
        return context


class CadastroListView(LoginRequiredMixin, ListView):
    template_name = 'cadastro_list.html'
    model = SiscoriUnknownData
    context_object_name = 'search_query'

    def get_queryset(self):
        query = super(CadastroListView, self).get_queryset()
        if self.request.GET.get('search'):
            search = self.request.GET.get('search')
            search_query = SiscoriUnknownData.objects.filter(description__icontains=search).order_by('month')
            query = search_query
        else:
            query = None
        return query

# TODO: Arrumar as escritas e como o programa compara os itens


class CadastroListFormView(LoginRequiredMixin, CreateView):
    template_name = 'cadastro_list_form.html'
    model = SiscoriUnknownData
    form_class = CadastroListForm
    success_url = reverse_lazy('cadastro_list_form')

    def get_context_data(self, **kwargs):
        context = super(CadastroListFormView, self).get_context_data(**kwargs)

        nome_prod = self.request.GET.get('nome_prod')
        marca = self.request.GET.get('marca')
        cod_marca = self.request.GET.get('cod_marca')
        descricao = self.request.GET.get('descricao')
        chaves = self.request.GET.get('keywords')
        query = SiscoriUnknownData.objects.get(pk=self.kwargs['pk'])

        if nome_prod:
            message_success = validate_and_set_new_infos(new_query=query, nome_prod=nome_prod, marca=marca,
                                                         cod_marca=cod_marca, descricao=descricao, chaves=chaves)
            context['message_success'] = message_success
        context['description'] = query.description
        return context


class AdminSiscoFiltrosView(LoginRequiredMixin, TemplateView):
    template_name = 'admin_filtros.html'

    def get_context_data(self, **kwargs):
        context = super(AdminSiscoFiltrosView, self).get_context_data(**kwargs)
        plan_pk = kwargs.get('pk')
        query = SiscoriFiles.objects.get(pk=plan_pk)
        context['query'] = query
        return context


class RegistrosUnknownView(LoginRequiredMixin, ListView):
    template_name = 'registros_unknown.html'
    model = SiscoriUnknownData
    paginate_by = 50
    ordering = ['month']


class RegistrosInfosView(LoginRequiredMixin, ListView):
    template_name = 'registros_infos.html'
    model = Infos
    paginate_by = 50
    ordering = ['marca']





