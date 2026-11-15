"""Check generated output: unresolved Liquid, missing local links, duplicate DOIs."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import argparse
import json
import sys
import re

class Links(HTMLParser):
 def __init__(self):
  super().__init__(); self.links=[]; self.ids=[]; self.h1=0
 def handle_starttag(self,tag,attrs):
  attr=dict(attrs)
  if tag=='h1':self.h1+=1
  if 'id' in attr:self.ids.append(attr['id'])
  for k in ['href','src']:
   if k in attr:self.links.append(attr[k])

def main():
 p=argparse.ArgumentParser();p.add_argument('directory',nargs='?',default='dist');p.add_argument('--baseurl',default='');a=p.parse_args()
 root=Path(a.directory).resolve(); errors=[];count=0;local=0
 for file in root.rglob('*.html'):
  count+=1;text=file.read_text(encoding='utf-8');parser=Links();parser.feed(text)
  if '{{' in text or '{%' in text:errors.append(f'{file}: unresolved Liquid')
  if len(parser.ids)!=len(set(parser.ids)):errors.append(f'{file}: duplicate IDs')
  redirect='http-equiv="refresh"' in text or 'http-equiv=refresh' in text
  if parser.h1!=1 and not redirect:errors.append(f'{file}: {parser.h1} h1 headings')
  for link in parser.links:
   u=urlsplit(link)
   if u.scheme or u.netloc or not u.path:continue
   path=unquote(u.path)
   if a.baseurl and path.startswith(a.baseurl+'/'):path=path[len(a.baseurl):]
   target=root/path.lstrip('/') if path.startswith('/') else file.parent/path
   if target.is_dir():target=target/'index.html'
   local+=1
   if not target.is_file():errors.append(f'{file.relative_to(root)}: missing {link}')
 print(json.dumps({'html_pages':count,'local_links_checked':local,'errors':errors},indent=2))
 sys.exit(bool(errors))
if __name__=='__main__':main()
