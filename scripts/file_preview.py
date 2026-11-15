"""Prepare file:// navigation for visual review without opening a local port."""
from pathlib import Path
import re
import shutil
root=Path(__file__).resolve().parents[1]
out=root/'previews'
shutil.copytree(root/'dist',out,dirs_exist_ok=True)
prefix=out.as_uri()
for file in out.rglob('*.html'):
 text=file.read_text(encoding='utf-8')
 text=re.sub(r'(href|src)="(/[^"#?]*)([?#][^"]*)?"',lambda m:m[1]+'="'+prefix+m[2]+('index.html' if m[2].endswith('/') else '')+(m[3] or '')+'"',text)
 file.write_text(text,encoding='utf-8')
print((out/'index.html').as_uri())
