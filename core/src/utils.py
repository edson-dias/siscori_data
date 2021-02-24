import csv


def csv_reading(file, delimiter):
    data = []
    with open(file, encoding='latin-1') as _file:
        csv_temp = csv.reader(_file, delimiter=delimiter)
        csv.field_size_limit(100000000)

        for row in csv_temp:
            data.append(row)
        return data


def set_del(data, colunas_del=None):
    if not colunas_del:
        colunas_del = [0, 2, 2, 3, 4, 4, 4, 5, 5, 5, 5, 5, 7, 7, 8, 8, 8]

    try:
        for row in data:
            for col in colunas_del:
                del row[col]
            for j in range(len(row)):
                row[j] = row[j].strip()
    except IndexError:
        # TODO:Criar função que contabilize quantas colunas tem na planilha e retorne um valor, sugerindo a correção.
        print('Número inválido para remoção de colunas!')
    return data


def set_filtro(data, ncm_list, countries_list, sec_countries_list=None):
    if sec_countries_list is None:
        sec_countries_list = countries_list

    filtered_data = []

    [filtered_data.append(row_csv) for row_csv in data for ncm_number in ncm_list if ncm_number in row_csv[1]
     for country in countries_list if country in row_csv[2].capitalize()
     for row in sec_countries_list if row in row_csv[3].capitalize()]

    return tuple(filtered_data)


def convert_string_to_list(string, char_to_remove=None):

    if char_to_remove is None:
        char_to_remove = ['[', ']', "'"]

    for character in char_to_remove:
        string = string.replace(character, '')

    string_list = string.split(',')

    for i, word in enumerate(string_list):
        string_list[i] = word.strip()

    return string_list
