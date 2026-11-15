"""Local preview of the lab's Liquid templates when Ruby is unavailable.

Uses the same layouts, content, and assets as Jekyll. This intentionally supports
only the Liquid tags used by this lab. The authoritative build runs in GitHub CI.
Requires the existing Python packages PyYAML and Jinja2.
"""
from pathlib import Path
import argparse
import datetime as dt
import html
import re
import shutil
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import yaml
from jinja2 import Environment, DictLoader

ROOT = Path(__file__).resolve().parents[1]

def frontmatter(path):
 text = path.read_text(encoding='utf-8')
 if text.startswith('---\n'):
  _, head, body = text.split('---', 2)
  return yaml.safe_load(head) or {}, body.lstrip('\n')
 return {}, text

def md(text):
 # The authored news/course bodies use only paragraphs, links, and emphasis.
 text = html.escape(text)
 text = re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+)\)', r'<a href="\2">\1</a>', text)
 text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
 return '\n'.join('<p>'+p.replace('  \n','<br>\n').replace('\n',' ')+'</p>' for p in text.strip().split('\n\n') if p.strip())

def expression(expr):
 expr = re.sub(r'([\w.]+)\.size\b', r'(\1 | length)', expr.strip())
 expr = re.sub(r'([\w.]+)\s+contains\s+([\w.]+)', r'\2 in \1', expr)
 # Convert Liquid filter arguments to Jinja calls without changing quoted pipes.
 parts = re.split(r'\s*\|\s*(?=(?:[^\x27]*\x27[^\x27]*\x27)*[^\x27]*$)', expr)
 result = parts[0]
 for part in parts[1:]:
  name, sep, args = part.partition(':')
  result += ' | '+name.strip()+('('+args.strip()+')' if sep else '')
 return result

def translate(text):
 def token(m):
  raw = m.group(0)
  if raw.startswith('{{'):
   return '{{ '+expression(raw[2:-2])+' }}'
  tag = raw[2:-2].strip()
  if tag.startswith('assign '):
   name, expr = tag[7:].split('=',1)
   return '{% set '+name.strip()+' = '+expression(expr)+' %}'
  if tag.startswith('include '):
   return "{% include '"+tag[8:].strip()+"' %}"
  if tag.startswith('for '):
   match = re.match(r'for (\w+) in (.+?)(?: limit:\s*(\d+))?$',tag)
   name, value, limit = match.groups()
   value = expression(value)
   if limit:
    value = '('+value+')[:'+limit+']'
   return '{% for '+name+' in '+value+' %}'
  if tag.startswith('if '):
   return '{% if '+expression(tag[3:])+' %}'
  return '{% '+tag+' %}'
 return re.sub(r'{{.*?}}|{%.*?%}', token, text, flags=re.S)

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('--baseurl',default='')
 parser.add_argument('--output',default='dist')
 args=parser.parse_args()
 dest=ROOT/args.output
 if dest.resolve()==ROOT.resolve() or not dest.resolve().is_relative_to(ROOT.resolve()):
  raise ValueError('Output must be a subdirectory inside the project')
 dest.mkdir(exist_ok=True,parents=True)
 site=yaml.safe_load((ROOT/'_config.yml').read_text(encoding='utf-8'))
 site['baseurl']=args.baseurl.rstrip('/')
 try:
  timezone=ZoneInfo(site.get('timezone','UTC'))
 except ZoneInfoNotFoundError:
  timezone=dt.timezone.utc
 site['time']=dt.datetime.now(timezone)
 site['data']={p.stem:yaml.safe_load(p.read_text(encoding='utf-8')) for p in (ROOT/'_data').glob('*.yml')}
 pages=[]
 for folder in ['_pages','_publications','_teaching','_news']:
  docs=[]
  for path in sorted((ROOT/folder).glob('*')):
   if path.suffix not in ['.md','.html']:
    continue
   meta,body=frontmatter(path)
   if not site.get('future',False) and meta.get('date'):
    date=meta['date']
    if isinstance(date,str):
     date=dt.datetime.fromisoformat(date.replace('Z','+00:00'))
    if not isinstance(date,dt.datetime):
     date=dt.datetime.combine(date,dt.time.min)
    if date.tzinfo is None:
     date=date.replace(tzinfo=timezone)
    if date > site['time']:
     continue
   kind=folder.lstrip('_')
   defaults={'pages':'lab-page','publications':'lab-publication','teaching':'lab-course','news':'lab-news'}
   meta.setdefault('layout',defaults[kind])
   meta['url']=meta.get('permalink',f'/{kind}/{path.stem}/')
   meta['_body']=body if path.suffix=='.html' else md(body)
   docs.append(meta)
  site[folder.lstrip('_')]=docs
  pages.extend(docs)
 templates={}
 for p in (ROOT/'_includes').rglob('*.html'):
  templates[str(p.relative_to(ROOT/'_includes')).replace('\\','/')]=translate(p.read_text(encoding='utf-8'))
 layouts={p.stem:frontmatter(p) for p in (ROOT/'_layouts').glob('lab*.html')}
 env=Environment(loader=DictLoader(templates),autoescape=False)
 env.filters.update({
  'relative_url':lambda s:str(s) if urlsplit(str(s or '')).scheme or str(s or '').startswith('//') else site['baseurl']+'/'+str(s or '').lstrip('/'),
  'absolute_url':lambda s:str(s) if urlsplit(str(s or '')).scheme or str(s or '').startswith('//') else site['url']+site['baseurl']+'/'+str(s or '').lstrip('/'),
  'escape':lambda s:html.escape(str(s or ''),quote=True),
  'default':lambda x,d: x if x else d,
  'where':lambda xs,k,v:[x for x in xs if x.get(k)==v],
  'sort':lambda xs,key=None:sorted(xs,key=lambda x:str(x.get(key,'')) if key else x),
  'reverse':lambda xs:list(reversed(list(xs))),
  'map':lambda xs,k:[x.get(k) for x in xs],
  'uniq':lambda xs:list(dict.fromkeys(xs)),
  'date':lambda d,f:(dt.datetime.fromisoformat(str(d)) if isinstance(d,str) else d).strftime(f),
 })
 for page in pages:
  result=env.from_string(translate(page['_body'])).render(site=site,page=page)
  layout=page['layout']
  seen=set()
  while layout:
   if layout in seen:
    raise ValueError('Recursive layout '+layout)
   seen.add(layout)
   meta,body=layouts[layout]
   result=env.from_string(translate(body)).render(site=site,page=page,content=result)
   layout=meta.get('layout')
  url=page['url'].lstrip('/')
  target=dest/(url if url.endswith('.html') else url+'index.html')
  target.parent.mkdir(exist_ok=True,parents=True)
  target.write_text(result,encoding='utf-8')
  for old in page.get('redirect_from',[]):
   redirect=dest/old.lstrip('/')/'index.html'
   redirect.parent.mkdir(exist_ok=True,parents=True)
   actual=site['baseurl']+page['url']
   redirect.write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Page moved</title><meta http-equiv="refresh" content="0;url={actual}"></head><body><a href="{actual}">Continue</a></body></html>',encoding='utf-8')
 for name in ['assets','images']:
  shutil.copytree(ROOT/name,dest/name,dirs_exist_ok=True)
 print(f'Built {len(pages)} pages at {dest} (local preview; GitHub CI uses Jekyll).')

if __name__=='__main__':
 main()
