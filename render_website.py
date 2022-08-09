import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    os.makedirs('docs', exist_ok=True)

    last_page = len(pages)
    for current_page_number, page in enumerate(pages, 1):
        rendered_page = template.render(books=chunked(page, 2),
                                        current_page=current_page_number,
                                        previous_page=current_page_number - 1,
                                        next_page=current_page_number + 1,
                                        last_page=last_page)
        if current_page_number == 1:
            with open('docs/index.html', 'w', encoding="utf8") as file:
                file.write(rendered_page)
        else:
            with open(f'docs/index{current_page_number}.html', 'w', encoding="utf8") as file:
                file.write(rendered_page)


with open('docs/static/parse_result/fantastic_books_catalog.json', encoding='utf-8') as f:
    books = json.load(f)

if books and '\\' in books[0]['image_src']:
    for book in books:
        if book.get('book_path'):
            dir_, book_dir, filename = book['book_path'].split('\\')
            book['book_path'] = f'{dir_}/{book_dir}/{filename}'
        if book.get('image_src'):
            dir_, image_dir, filename = book['image_src'].split('\\')
            book['image_src'] = f'{dir_}/{image_dir}/{filename}'

pages = list(chunked(books, 10))

on_reload()

server = Server()

server.watch('template.html', on_reload)

server.serve(root='docs/', default_filename='index.html')
