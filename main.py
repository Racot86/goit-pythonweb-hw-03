#task
#За аналогією з розглянутим прикладом у конспекті, створіть веб-додаток з маршрутизацією для двох html сторінок: index.html та message.html.
#Обробіть під час роботи програми статичні ресурси: style.css, logo.png;
#Організуйте роботу з формою на сторінці message.html;
#У разі виникнення помилки 404 Not Found повертайте сторінку error.html
#Ваша програма працює на порту 3000
#При роботі з формою отриманий байт-рядок перетворюємо у словник і зберігаємо його в json файл data.json в директорію storage.

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import mimetypes
import pathlib
import json
from datetime import datetime


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message':
            self.send_html_file('message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        data_parse = urllib.parse.unquote_plus(data.decode())
        data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
        print(data_dict)

        storage_dir = pathlib.Path("storage")
        storage_dir.mkdir(exist_ok=True)
        data_file = storage_dir / "data.json"

        if data_file.exists():
            with open(data_file, 'r', encoding='utf-8') as f:
                messages = json.load(f)
        else:
            messages = {}

        timestamp = datetime.now().isoformat()
        messages[timestamp] = {
            "username": data_dict.get("username", "Anonymous"),
            "message": data_dict.get("message", "")
        }

        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)

        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        try:
            with open(filename, 'rb') as fd:
                self.wfile.write(fd.read())
        except BrokenPipeError:
            print("Client disconnected before response was fully sent.")

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()

if __name__ == '__main__':
    run()
