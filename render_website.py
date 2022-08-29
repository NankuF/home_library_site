import json
import os
from functools import partial

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

JSON_FILENAME = 'fantastic_books_catalog.json'


def on_reload(pages):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    os.makedirs('static/pages', exist_ok=True)

    last_page = len(pages)
    for current_page_number, page in enumerate(pages, 1):
        rendered_page = template.render(books=chunked(page, 2),
                                        current_page=current_page_number,
                                        last_page=last_page)
        current_page = 'index.html' if current_page_number == 1 else f'index{current_page_number}.html'
        with open(f'static/pages/{current_page}', 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    with open(f'parse_result/{JSON_FILENAME}', encoding='utf-8') as f:
        books = json.load(f)

    if books and '\\' in books[0]['image_src']:
        for book in books:
            if book.get('book_path'):
                dir_, book_dir, filename = book['book_path'].split('\\')
                book['book_path'] = f'{dir_}/{book_dir}/{filename}'
            if book.get('image_src'):
                dir_, image_dir, filename = book['image_src'].split('\\')
                book['image_src'] = f'{dir_}/{image_dir}/{filename}'

    books_per_page = 10
    pages = list(chunked(books, books_per_page))

    on_reload(pages)

    server = Server()

    on_reload_callback = partial(on_reload, pages)
    server.watch('template.html', func=on_reload_callback)

    server.serve(root='', default_filename='index.html')


if __name__ == '__main__':
    main()
