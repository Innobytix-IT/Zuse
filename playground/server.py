# FILE: playground/server.py
# Einfacher HTTP-Server für den Zuse Playground.
# Startet einen lokalen Server im Zuse-Hauptverzeichnis.
# Nutzung: python playground/server.py [port]

import http.server
import os
import sys

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

    # Wechsle ins Zuse-Hauptverzeichnis (eine Ebene hoch)
    zuse_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(zuse_dir)

    handler = http.server.SimpleHTTPRequestHandler
    handler.extensions_map.update({
        '.js': 'application/javascript',
        '.json': 'application/json',
        '.py': 'text/plain',
    })

    with http.server.HTTPServer(("", port), handler) as httpd:
        print(f"Zuse Playground laeuft auf: http://localhost:{port}/playground/")
        print(f"Serving files from: {zuse_dir}")
        print("Ctrl+C zum Beenden")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer beendet.")

if __name__ == "__main__":
    main()
