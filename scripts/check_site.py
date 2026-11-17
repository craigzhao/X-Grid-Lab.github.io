"""Validate authored publication data, generated pages, and local link targets."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import argparse
import datetime as dt
import json
import re
import sys

import yaml


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = []
        self.h1 = 0
        self.redirect = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'h1':
            self.h1 += 1
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a' and attrs.get('name'):
            self.ids.append(attrs['name'])
        if tag == 'meta' and attrs.get('http-equiv', '').lower() == 'refresh':
            self.redirect = True
        for key in ['href', 'src']:
            if attrs.get(key):
                self.links.append(attrs[key])


def check_publications(source, errors):
    """Catch content mistakes before a routine GitHub edit is deployed."""
    seen = {'doi': {}, 'pub_id': {}}
    required = ['title', 'pub_id', 'date', 'year', 'category', 'authors', 'venue', 'citation']
    categories = ['Journal', 'Conference', 'Preprint', 'Presentation', 'Thesis', 'Report']
    publications = sorted((source / '_publications').glob('*.md'))
    if not publications:
        errors.append(f'{source}: no publication source files found')
    for path in publications:
        label = str(path.relative_to(source))
        try:
            text = path.read_text(encoding='utf-8')
            if not text.startswith('---\n'):
                raise ValueError('missing YAML front matter')
            data = yaml.safe_load(text.split('---', 2)[1])
            if not isinstance(data, dict):
                raise ValueError('front matter must be a mapping')
            missing = [key for key in required if not data.get(key)]
            if missing:
                errors.append(f'{label}: missing required fields: {", ".join(missing)}')
            if data.get('category') not in categories:
                errors.append(f'{label}: category must be one of {", ".join(categories)}')
            if not data.get('doi') and not data.get('source_url'):
                errors.append(f'{label}: every item requires a DOI or source_url')
            if data.get('pub_id') and not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', str(data['pub_id'])):
                errors.append(f'{label}: pub_id must be a lowercase hyphenated identifier')
            if data.get('doi') and not re.fullmatch(r'10\.\d{4,9}/\S+', str(data['doi']), re.I):
                errors.append(f'{label}: doi must contain the DOI identifier, without a URL prefix')
            for key in ['source_url', 'scholar_url']:
                if data.get(key):
                    value = str(data[key])
                    url = urlsplit(value)
                    if url.scheme not in ['http', 'https'] or not url.netloc or re.search(r'\s', value):
                        errors.append(f'{label}: {key} must be a valid public HTTP(S) URL')
            if data.get('date') and data.get('year'):
                date = data['date']
                if isinstance(date, str):
                    date = dt.datetime.fromisoformat(date.replace('Z', '+00:00'))
                if date.year != int(data['year']):
                    errors.append(f'{label}: date and year disagree')
            for key in seen:
                value = str(data.get(key, '')).strip().lower()
                if not value:
                    continue
                if value in seen[key]:
                    errors.append(f'{label}: duplicate {key} also found in {seen[key][value]}')
                seen[key][value] = label
        except (ValueError, TypeError, AttributeError, yaml.YAMLError) as error:
            errors.append(f'{label}: invalid front matter: {error}')
    return len(publications)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', nargs='?', default='dist')
    parser.add_argument('--baseurl', default='')
    parser.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = Path(args.directory).resolve()
    baseurl = args.baseurl.rstrip('/')
    errors = []
    local = 0
    fragments = 0
    publication_count = check_publications(args.source.resolve(), errors)
    parsed = {}
    if not (root / 'index.html').is_file():
        errors.append(f'{root}: missing site index.html')
    for file in sorted(root.rglob('*.html')):
        text = file.read_text(encoding='utf-8')
        links = Links()
        links.feed(text)
        parsed[file.resolve()] = links
        label = str(file.relative_to(root))
        if '{{' in text or '{%' in text:
            errors.append(f'{label}: unresolved Liquid')
        if len(links.ids) != len(set(links.ids)):
            errors.append(f'{label}: duplicate IDs')
        if links.h1 != 1 and not links.redirect:
            errors.append(f'{label}: {links.h1} h1 headings')
    for file, page in parsed.items():
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                continue
            path = unquote(url.path)
            if baseurl and path.startswith('/'):
                if path == baseurl:
                    path = '/'
                elif path.startswith(baseurl + '/'):
                    path = path[len(baseurl):]
                else:
                    errors.append(f'{file.relative_to(root)}: local URL lacks baseurl {baseurl}: {link}')
                    continue
            target = root / path.lstrip('/') if path.startswith('/') else file.parent / path if path else file
            target = target.resolve()
            if target.is_dir():
                target = target / 'index.html'
            local += 1
            if not target.is_relative_to(root) or not target.is_file():
                errors.append(f'{file.relative_to(root)}: missing local target {link}')
            elif url.fragment and target.suffix == '.html':
                fragments += 1
                if unquote(url.fragment) not in parsed[target].ids:
                    errors.append(f'{file.relative_to(root)}: missing fragment target {link}')
    print(json.dumps({
        'publication_sources_checked': publication_count,
        'html_pages': len(parsed),
        'local_links_checked': local,
        'fragments_checked': fragments,
        'errors': errors,
    }, indent=2))
    sys.exit(bool(errors))


if __name__ == '__main__':
    main()
