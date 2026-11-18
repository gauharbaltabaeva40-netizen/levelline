"""Resize big site images to <=900px wide WebP and rewrite references."""
import os, re, shutil, subprocess, sys
from PIL import Image

SITE, BACKUP = sys.argv[1], sys.argv[2]
MAXW = 900
renames = {}
before = after = 0

for root, _, files in os.walk(os.path.join(SITE, "images")):
    if "/thumbs" in root:
        continue
    for f in files:
        if not f.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        src = os.path.join(root, f)
        rel = os.path.relpath(src, SITE)
        dst = os.path.splitext(src)[0] + ".webp"
        w = Image.open(src).size[0]
        cmd = ["cwebp", "-quiet", "-q", "82", "-alpha_q", "90", "-m", "6"]
        if w > MAXW:
            cmd += ["-resize", str(MAXW), "0"]
        subprocess.run(cmd + [src, "-o", dst], check=True)
        before += os.path.getsize(src)
        after += os.path.getsize(dst)
        bk = os.path.join(BACKUP, rel)
        os.makedirs(os.path.dirname(bk), exist_ok=True)
        shutil.move(src, bk)
        renames[rel] = os.path.relpath(dst, SITE)

for name in ("index.html",) + tuple(
        os.path.join("css", c) for c in os.listdir(os.path.join(SITE, "css"))):
    p = os.path.join(SITE, name)
    text = open(p, encoding="utf-8").read()
    n = 0
    for old, new in renames.items():
        # CSS files reference images relative to css/ ("../images/...")
        c = text.count(old)
        text = text.replace(old, new)
        n += c
    if n:
        open(p, "w", encoding="utf-8").write(text)
        print(f"{name}: {n} refs updated")

print(f"{len(renames)} images: {before/1e6:.1f} MB -> {after/1e6:.1f} MB")
