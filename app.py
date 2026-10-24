#!/usr/bin/env python3
"""A dependency-free system dashboard for Raspberry Pi OS."""
import argparse
import json
from pathlib import Path
import shutil
import socket
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PAGE = Path(__file__).with_name('index.html')


def read_number(path):
    try:
        return float(Path(path).read_text().strip())
    except (OSError, ValueError):
        return None


def stats():
    temperature = read_number('/sys/class/thermal/thermal_zone0/temp')
    uptime = None
    try:
        uptime = float(Path('/proc/uptime').read_text().split()[0])
    except (OSError, ValueError, IndexError):
        pass
    memory = {}
    try:
        for line in Path('/proc/meminfo').read_text().splitlines():
            key, value = line.split(':', 1)
            memory[key] = int(value.strip().split()[0]) * 1024
    except (OSError, ValueError, IndexError):
        pass
    total = memory.get('MemTotal')
    available = memory.get('MemAvailable')
    disk = shutil.disk_usage('/')
    return {
        'hostname': socket.gethostname(),
        'temperature_c': temperature / 1000 if temperature is not None else None,
        'uptime_seconds': uptime,
        'memory_total': total,
        'memory_used': total - available if total is not None and available is not None else None,
        'disk_total': disk.total,
        'disk_used': disk.used,
        'updated_at': int(time.time()),
    }


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split('?', 1)[0]
        if path == '/':
            data, content_type = PAGE.read_bytes(), 'text/html; charset=utf-8'
        elif path == '/api/stats':
            data = json.dumps(stats()).encode()
            content_type = 'application/json'
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='127.0.0.1', help='Use 0.0.0.0 for access on your home network')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print('Dashboard listening on {}:{}'.format(args.host, args.port), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
