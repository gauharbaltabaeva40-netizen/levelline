"""Download a Tilda page and all its Tilda-CDN assets, rewrite links to local paths."""
import os, re, sys, urllib.request, urllib.parse

SRC_URL, OUT = sys.argv[1], sys.argv[2]
UA = {"User-Agent": "Mozilla/5.0"}
CDN = r"https?://(?:static|neo|thb)\.tildacdn\.(?:pro|com)/[^\"'\s)<>&\\]+"
cache = {}


def fetch(url):
    import subprocess
    return subprocess.run(["curl", "-sfL", "--compressed", "--max-time", "60", "-A", UA["User-Agent"], url],
                          check=True, capture_output=True).stdout


def local_path(url):
    p = urllib.parse.urlparse(url)
    host, path = p.netloc, p.path.lstrip("/")
    if host.startswith("thb."):
        return "images/thumbs/" + path.replace("/-/resize/", "/resize-")
    if path.startswith(("tild", "tila")):
        return "images/" + path
    if path.startswith("ws/"):  # project-specific bundle
        return ("css/" if path.endswith(".css") else "js/") + os.path.basename(path)
    return path  # css/..., js/..., img/...


def grab(url, depth=0):
    url = url.split("?")[0]
    if url in cache:
        return cache[url]
    rel = local_path(url)
    cache[url] = rel
    dest = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    try:
        data = fetch(url)
    except Exception as e:
        print("FAIL", url, e)
        cache[url] = None
        return None
    if rel.endswith(".css") and depth < 2:
        text = data.decode("utf-8", "replace")
        base = os.path.dirname(rel)
        def sub(m):
            r = grab(m.group(0), depth + 1)
            return os.path.relpath(r, base) if r else m.group(0)
        text = re.sub(CDN, sub, text)
        data = text.encode("utf-8")
    with open(dest, "wb") as f:
        f.write(data)
    print("OK  ", rel)
    return rel


html = fetch(SRC_URL).decode("utf-8")
html = re.sub(CDN, lambda m: grab(m.group(0)) or m.group(0), html)
html = html.replace("https://levelline.tilda.ws/main", "./")
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("done:", len(cache), "assets")
