#!/usr/bin/env python3
"""Regenerate sitemap.xml from the live database (or a local copy of it).

    python3 scripts/generate-sitemap.py                    # reads https://database-34a.pages.dev
    python3 scripts/generate-sitemap.py --db ../database   # reads a local clone of the database repo

Lists the 7 main pages plus one URL per project and per poster (each has its own ?view=<id> page with its own title,
description and canonical URL - see seoForDetail() in app.js). Run it after adding/removing projects or posters in the
admin panel, then commit sitemap.xml. Standard library only.
"""
import argparse, datetime, json, pathlib, urllib.request
from xml.sax.saxutils import escape

BASE = 'https://munakhan.pages.dev'
DB = 'https://database-34a.pages.dev'
PAGES = ['/', '/my-story/', '/education-experience/', '/projects/', '/publications/', '/conferences/', '/posters/']

ap = argparse.ArgumentParser()
ap.add_argument('--db', help='folder holding projects.json and posters.json (default: fetch from the live database)')
args = ap.parse_args()

def load(name):
    if args.db:
        return json.loads(pathlib.Path(args.db, name).read_text(encoding='utf-8'))
    with urllib.request.urlopen(f'{DB}/{name}', timeout=20) as r:
        return json.loads(r.read().decode('utf-8'))

urls = list(PAGES)
for fname, key, page in (('projects.json', 'projects', '/projects/'), ('posters.json', 'posters', '/posters/')):
    for item in load(fname).get(key, []):
        if item.get('id'):
            urls.append(f"{page}?view={item['id']}")

today = datetime.date.today().isoformat()
body = '\n'.join(f'  <url>\n    <loc>{escape(BASE + u)}</loc>\n    <lastmod>{today}</lastmod>\n  </url>' for u in urls)
out = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n'
pathlib.Path(__file__).resolve().parent.parent.joinpath('sitemap.xml').write_text(out, encoding='utf-8')
print(f'sitemap.xml written with {len(urls)} URLs')
