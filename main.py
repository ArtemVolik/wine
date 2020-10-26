# -*- coding: utf-8 -*-
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
import pandas as pd
from collections import defaultdict
import argparse


parser = argparse.ArgumentParser(description="Программа импортирует товары из excel, при\
указании ошибочного/и или \"неправильного\" файла будет использован импорт из дефолтного файла \"goods_excel\"")
parser.add_argument('file_path', help='для изменения каталога введите путь/имя файла', nargs='?',
                    default='goods_excel.xlsx')
args = parser.parse_args()
raw_data_from_excel = pd.read_excel(args.file_path, keep_default_na=False)
raw_data_from_excel.rename(
    columns={'Категория': 'category', 'Название': 'name', 'Сорт': 'sort', 'Цена': 'price', 'Картинка': 'image',
             'Акция': 'sale'}, inplace=True)
goods_catalog = raw_data_from_excel.to_dict(orient='records')
category_grouped_goods_catalog = defaultdict(list)
for i in goods_catalog:
    category_grouped_goods_catalog[i['category']].append(i)

"""jinja не дает перебрать словарь без преобразования типов данных указанного ниже, 
category_grouped_goods_list - воспринимаеся каксписок и не дает доступа к значениям"""

category_grouped_goods_dict = dict(category_grouped_goods_catalog)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')
founded = datetime.today().year - 1920

rendered_page = template.render(
    date=founded,
    goods_dict=category_grouped_goods_dict
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
