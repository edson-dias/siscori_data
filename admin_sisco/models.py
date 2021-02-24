from django.db import models
from django.core.validators import FileExtensionValidator
from django.db.models.base import ObjectDoesNotExist, MultipleObjectsReturned
from core.models import Infos, ValoresMensais, KeywordSiscori
from core.src import utils
import os


class SiscoriFiles(models.Model):
    files = models.FileField(upload_to='siscori_files', validators=[FileExtensionValidator(['csv'])])

    def __str__(self):
        return f'{self.files}'

    def delete(self, *args, **kwargs):
        self.files.delete()
        super().delete(*args, **kwargs)


class SiscoriHistory(models.Model):
    files = models.CharField('files', max_length=100)
    n_filters = models.CharField('n_filters', max_length=500)
    c_filters = models.CharField('c_filters', max_length=500)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.date}: {self.files}'


class NcmSiscoriFilter(models.Model):
    ncm_filters = models.CharField('ncm_filters', max_length=100)

    def __str__(self):
        return f'{self.ncm_filters}'


class CountrySiscoriFilter(models.Model):
    countries_filters = models.CharField('countries_filter', max_length=100)

    def __str__(self):
        return f'{self.countries_filters}'


class SiscoriUnknownData(models.Model):
    description = models.TextField('description', max_length=4000)
    ncm = models.CharField('ncm', max_length=50)
    harbor = models.CharField('harbor', max_length=50)
    purchase_country = models.CharField('purchase_country', max_length=50)
    origin_country = models.CharField('origin_country', max_length=50)
    month = models.IntegerField('month')
    year = models.IntegerField('year')
    quantity = models.IntegerField('quantity')
    value = models.FloatField('value', max_length=50)


def validate_and_set_new_infos(**kwargs):
    query = kwargs['new_query']
    new_code = kwargs['cod_marca']
    keywords = kwargs['chaves']

    try:
        validate = Infos.objects.get(cod_marca=new_code)

    except ObjectDoesNotExist:
        _set_new_infos(**kwargs)
        return 'Item registrado com sucesso!'

    except MultipleObjectsReturned:
        return 'Mais de um registro encontrado na base. Verificar banco de dados.'

    else:
        new_values = ValoresMensais(infos_prod=validate, mes=query.month, ano=query.year,
                                    quant=query.quantity, valor=query.value)
        new_values.save()

        new_keyword = KeywordSiscori(infos_prod=validate, keywords=keywords)
        new_keyword.save()
        pk_already_in_db = query.id
        _check_equals_registers(new_keyword, pk_exclude=pk_already_in_db)
        query.delete()
        return 'Produto já cadastrado no banco de dados, palavra chave registrada com sucesso!'


def _set_new_infos(**kwargs):
    new_query = kwargs['new_query']
    nome_prod = kwargs['nome_prod']
    marca = kwargs['marca']
    cod_marca = kwargs['cod_marca']
    descricao = kwargs['descricao']
    chaves = kwargs['chaves']

    new_item_infos = Infos(nome_prod=nome_prod, marca=marca, cod_marca=cod_marca, descricao=descricao,
                           ncm=new_query.ncm, porto=new_query.harbor, pa=new_query.purchase_country,
                           po=new_query.origin_country)
    new_item_infos.save()
    new_item_values = ValoresMensais(infos_prod=new_item_infos, mes=new_query.month, ano=new_query.year,
                                     quant=new_query.quantity, valor=new_query.value)
    new_item_values.save()

    new_item_keys = KeywordSiscori(infos_prod=new_item_infos, keywords=chaves)
    new_item_keys.save()
    new_query.delete()
    _check_equals_registers(new_item_keys)


def _check_equals_registers(keyword_query):
    new_query = SiscoriUnknownData.objects.filter(description__icontains=keyword_query.keywords)
    if new_query:
        for register in new_query:
            new_register = ValoresMensais(infos_prod=keyword_query.infos_prod, mes=register.month, ano=register.year,
                                          quant=register.quantity, valor=register.value)
            new_register.save()
            register.delete()


def _set_data(plan_csv, ncm_filter, countries_filter, keys_database):

    # TODO: Verificar o nome do arquivo, pegar os filtros pertencentes àquela planilha
    # TODO: A comparação da chave com a descrição deve ser manipulada para eliminar acentos, capslock e etc...

    already_registered_in_db_flag = None
    file_path = os.path.join('media', str(plan_csv.files))

    data = utils.csv_reading(file_path, '@')
    data = utils.set_del(data)

    filtered_data = utils.set_filtro(data, ncm_list=ncm_filter, countries_list=countries_filter)

    for itens in filtered_data:
        if keys_database:
            for key in keys_database:
                if key.keywords in itens[4]:
                    pk = key.infos_prod.id
                    data_found = ValoresMensais(mes=itens[0][4:6], ano=itens[0][0:4],
                                                quant=int((float(itens[6].replace(',', '.')))),
                                                valor=float(itens[5].replace(',', '.')), infos_prod_id=pk)
                    data_found.save()
                    already_registered_in_db_flag = True

            if already_registered_in_db_flag is None:
                unknown_data = SiscoriUnknownData(year=itens[0][0:4], month=itens[0][4:6], ncm=itens[1],
                                                  origin_country=itens[2], purchase_country=itens[3],
                                                  description=itens[4],
                                                  value=float(itens[5].replace(',', '.')),
                                                  quantity=int((float(itens[6].replace(',', '.')))),
                                                  harbor=itens[7])
                unknown_data.save()
        else:
            unknown_data = SiscoriUnknownData(year=itens[0][0:4], month=itens[0][4:6], ncm=itens[1],
                                              origin_country=itens[2], purchase_country=itens[3],
                                              description=itens[4], value=float(itens[5].replace(',', '.')),
                                              quantity=int((float(itens[6].replace(',', '.')))),
                                              harbor=itens[7])
            unknown_data.save()

        already_registered_in_db_flag = None
    history = SiscoriHistory(files=plan_csv.files, n_filters=ncm_filter, c_filters=countries_filter)
    history.save()
    plan_csv.delete()
