from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
import pandas as pd
from collections import defaultdict



goods_raw = pd.read_excel('wine3.xlsx', keep_default_na = False)
goods_raw.rename(columns = {'Категория':'category','Название':'name', 'Сорт':'sort', 'Цена':'price', 'Картинка':'image', 'Акция':'sale'}, inplace = True)
goods_raw = goods_raw.to_dict(orient ='records')
goods_dict = defaultdict(list)
for i in goods_raw:
    goods_dict[i['category']].append(i)
goods_dict = dict(goods_dict)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)


template = env.get_template('template.html')
founded = datetime.today().year - 1920

rendered_page = template.render(
    date=founded,
    goods_dict=goods_dict
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()

