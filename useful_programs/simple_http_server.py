#!/usr/bin/env python3
"""Start a simple HTTP server serving the current directory.

Usage: python simple_http_server.py [port]
"""
import http.server
import socketserver
import sys


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving HTTP on 0.0.0.0:{port} (Ctrl-C to stop)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")


if __name__ == "__main__":
    main()
