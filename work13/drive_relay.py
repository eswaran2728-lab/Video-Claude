# Local byte-range relay for Drive: ffmpeg reads http://127.0.0.1:8765/<file_id> (plain HTTP, seekable). Upstream requests go
# to drive.usercontent.google.com via `requests` (honours HTTPS_PROXY + the proxy CA).
# Why: ffmpeg's own HTTPS requests stall behind the agent proxy here, and Drive answers open-ended ranges ("bytes=N-", what
# ffmpeg sends) with its quota/error page while bounded ranges are served. So every client request is answered as a 206
# assembled from bounded 8 MB upstream ranges. Nothing is written to disk.
import http.server, socketserver, requests, re, time
UP = "https://drive.usercontent.google.com/download?id={}&export=download&confirm=t"
CH = 8 << 20
S = requests.Session(); S.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) Chrome/126"
SIZES = {}


def fetch(fid, a, b):
    for attempt in range(6):
        try:
            r = S.get(UP.format(fid), headers={"Range": f"bytes={a}-{b}"}, timeout=120)
            if r.status_code == 206 and "text/html" not in r.headers.get("Content-Type", ""):
                return r
        except requests.RequestException:
            pass
        time.sleep(4 * (attempt + 1))
    return None


def size(fid):
    if fid not in SIZES:
        r = fetch(fid, 0, 0)
        if r is None: return None
        SIZES[fid] = int(r.headers["Content-Range"].split("/")[1])
    return SIZES[fid]


class H(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _go(self, head=False):
        fid = self.path.strip("/").split("?")[0]; total = size(fid)
        if total is None:
            self.send_error(502); return
        m = re.match(r"bytes=(\d*)-(\d*)", self.headers.get("Range", "") or "")
        a = int(m.group(1)) if m and m.group(1) else 0
        b = int(m.group(2)) if m and m.group(2) else total - 1
        b = min(b, total - 1)
        if a > b:
            self.send_response(416); self.send_header("Content-Range", f"bytes */{total}"); self.send_header("Content-Length", "0"); self.end_headers(); return
        self.send_response(206)
        self.send_header("Content-Type", "application/octet-stream"); self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {a}-{b}/{total}"); self.send_header("Content-Length", str(b - a + 1)); self.end_headers()
        if head: return
        p = a
        try:
            while p <= b:
                q = min(b, p + CH - 1); r = fetch(fid, p, q)
                if r is None: break
                self.wfile.write(r.content); p = q + 1
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_GET(self): self._go()
    def do_HEAD(self): self._go(True)
    def log_message(self, *a): pass


class T(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True


T(("127.0.0.1", 8765), H).serve_forever()
