from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import webbrowser


HOST = "127.0.0.1"
PORT = 8765
ROOT = Path(__file__).resolve().parent
ALLOWED_PATHS = {"/", "/index.html", "/leaderboard.json"}


class GameWebHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        if urlsplit(self.path).path not in ALLOWED_PATHS:
            self.send_error(404, "File not found.")
            return
        super().do_GET()


def main():
    server = ThreadingHTTPServer((HOST, PORT), GameWebHandler)
    print(f"Pudge Breakout website: http://{HOST}:{PORT}")
    webbrowser.open(f"http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nWebsite server stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
