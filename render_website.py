import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server

with open('parse_result/fantastic_books_catalog.json', encoding='utf-8') as f:
    books = json.load(f)

if books and '\\' in books[0]['image_src']:
    for book in books:
        if book.get('book_path'):
            dir_, book_dir, filename = book['book_path'].split('\\')
            book['book_path'] = f'{dir_}/{book_dir}/{filename}'
        if book.get('image_src'):
            dir_, image_dir, filename = book['image_src'].split('\\')
            book['image_src'] = f'{dir_}/{image_dir}/{filename}'


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(books=books)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    print("Site rebuilt")


on_reload()

server = Server()

server.watch('template.html', on_reload)

server.serve(root='.')
