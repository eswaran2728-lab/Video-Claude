# Local byte-range relay for Drive: ffmpeg reads http://127.0.0.1:8765/<file_id> (plain HTTP, seekable); each request is
# forwarded with its Range header to drive.usercontent.google.com via `requests` (honours HTTPS_PROXY + the proxy CA).
# Needed because ffmpeg's own HTTPS requests stall behind the agent proxy in this session. Nothing is written to disk.
import http.server, socketserver, requests, time
UP = "https://drive.usercontent.google.com/download?id={}&export=download&confirm=t"
S = requests.Session(); S.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) Chrome/126"


class H(http.server.BaseHTTPRequestHandler):
    def _go(self, head=False):
        fid = self.path.strip("/").split("?")[0]; hdr = {}
        if self.headers.get("Range"): hdr["Range"] = self.headers["Range"]
        for attempt in range(5):
            try:
                r = S.get(UP.format(fid), headers=hdr, stream=True, timeout=60)
                if r.status_code in (200, 206) and "text/html" not in r.headers.get("Content-Type", ""): break
                r.close()
            except requests.RequestException:
                pass
            time.sleep(3 * (attempt + 1))
        else:
            self.send_error(502); return
        self.send_response(r.status_code)
        for k in ("Content-Type", "Content-Length", "Content-Range"):
            if k in r.headers: self.send_header(k, r.headers[k])
        self.send_header("Accept-Ranges", "bytes"); self.end_headers()
        if head: r.close(); return
        try:
            for chunk in r.iter_content(1 << 20): self.wfile.write(chunk)
        except (BrokenPipeError, ConnectionResetError):
            pass
        finally:
            r.close()

    def do_GET(self): self._go()
    def do_HEAD(self): self._go(True)
    def log_message(self, *a): pass


class T(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True


T(("127.0.0.1", 8765), H).serve_forever()
