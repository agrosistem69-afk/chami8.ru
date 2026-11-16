#!/usr/bin/env python3
"""Подготовка сайта к выкладке (запускает .github/workflows/pages.yml).

Запуск: python3 .github/scripts/site_build.py <папка_сайта>
  <папка_сайта> — копия репозитория без .git, .github и _drafts (то, что уйдёт на хостинг).
  Сам репозиторий скрипт НЕ меняет: правки делаются только в копии для выкладки.

Что делает:
1. Статья, которую перенесли из _drafts/ в articles/ (например, SMM-сервис после одобрения),
   получает дату публикации = день, когда её папка появилась в articles/ (по Москве).
   Меняется только если дата в странице раньше (черновик собран заранее).
2. Если статьи нет в списке /articles/, добавляет в список карточку (заголовок, описание, картинка, дата).
3. Пишет sitemap-all.xml: основные страницы + все articles/*/index.html, кроме страниц с noindex;
   lastmod — дата последнего коммита файла по Москве (на хостинге GitHub Pages нет PHP,
   поэтому карта собирается здесь, при каждой выкладке).
"""
import datetime, html, json, os, re, subprocess, sys

SITE = "https://chami8.ru"
ARTICLES = "articles"
MSK = datetime.timezone(datetime.timedelta(hours=3))
MAIN_PAGES = ["index.html", "articles/index.html"]  # основные страницы, явный список
MONTHS = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа",
          "сентября", "октября", "ноября", "декабря"]


def git_date(path, first=False):
    """Дата коммита файла по Москве: последнего или (first=True) того, где файл появился по этому пути."""
    args = ["git", "log", "--format=%ct", "--no-renames"]
    if first:
        args += ["--diff-filter=A"]
    out = subprocess.run(args + ["--", path], capture_output=True, text=True).stdout.split()
    if not out:
        return None
    ts = int(out[-1] if first else out[0])
    return datetime.datetime.fromtimestamp(ts, MSK).date()


def noindex(text):
    m = re.search(r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']*)["\']', text, re.I)
    return bool(m and "noindex" in m.group(1).lower())


def ru_date(d):
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def fix_date(text, new):
    """Подставить дату публикации в метатеги, JSON-LD и строку с датой под заголовком."""
    m = re.search(r'<meta property="article:published_time" content="(\d{4}-\d\d-\d\d)">', text)
    if not m:
        return text, None
    old = datetime.date.fromisoformat(m.group(1))
    if new is None or new <= old:
        return text, old
    o, n = old.isoformat(), new.isoformat()
    text = text.replace(f'"article:published_time" content="{o}"', f'"article:published_time" content="{n}"')
    mm = re.search(r'<meta property="article:modified_time" content="(\d{4}-\d\d-\d\d)">', text)
    if mm and mm.group(1) < n:
        text = text.replace(f'"article:modified_time" content="{mm.group(1)}"', f'"article:modified_time" content="{n}"')
        text = re.sub(r'("dateModified":\s*")' + re.escape(mm.group(1)) + '"', r"\g<1>" + n + '"', text)
    text = re.sub(r'("datePublished":\s*")' + re.escape(o) + '"', r"\g<1>" + n + '"', text)
    text = text.replace(f'<time datetime="{o}">{ru_date(old)}</time>', f'<time datetime="{n}">{ru_date(new)}</time>')
    return text, new


def card(slug, text, date):
    def meta(name, attr="name"):
        m = re.search(rf'<meta {attr}="{name}" content="([^"]*)"', text)
        return m.group(1) if m else ""
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.S)
    h1 = re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else meta("og:title", "property")
    img = re.search(r'<img src="(/articles/img/[^"]+)" width="(\d+)" height="(\d+)"[^>]*alt="([^"]*)"', text)
    src, w, h, alt = img.groups() if img else ("/articles/img/photos/skala-pialy-nastoj.webp", "750", "1000",
                                               "Пиалы с настоем чая на камне")
    return f"""<!--POSTS-->
  <li>
    <img src="{src}" width="{w}" height="{h}" loading="lazy" alt="{alt}">
    <div class="tx">
      <h2><a href="/articles/{slug}/">{h1}</a></h2>
      <p>{meta("description")}</p>
      <p class="meta"><time datetime="{date.isoformat()}">{ru_date(date)}</time></p>
    </div>
  </li>""", h1


def main(out):
    urls = []
    for p in MAIN_PAGES:
        f = os.path.join(out, p)
        if os.path.isfile(f) and not noindex(open(f, encoding="utf-8").read()):
            loc = SITE + "/" + p[:-len("index.html")]
            urls.append((loc, git_date(p) or datetime.datetime.now(MSK).date()))

    idx_path = os.path.join(out, ARTICLES, "index.html")
    idx = open(idx_path, encoding="utf-8").read() if os.path.isfile(idx_path) else None
    added = []
    arts = []
    for slug in sorted(os.listdir(os.path.join(out, ARTICLES))):
        rel = f"{ARTICLES}/{slug}/index.html"
        f = os.path.join(out, rel)
        if not os.path.isfile(f):
            continue
        text = open(f, encoding="utf-8").read()
        new, pub = fix_date(text, git_date(rel, first=True))
        if new != text:
            open(f, "w", encoding="utf-8").write(new)
            print(f"дата публикации {rel} → {pub}")
        if noindex(new):
            print(f"пропущено (noindex): {rel}")
            continue
        last = git_date(rel) or datetime.datetime.now(MSK).date()
        arts.append((f"{SITE}/{ARTICLES}/{slug}/", max(last, pub or last)))
        if idx is not None and f'href="/{ARTICLES}/{slug}/"' not in idx and "<!--POSTS-->" in idx:
            c, h1 = card(slug, new, pub or last)
            idx = idx.replace("<!--POSTS-->", c, 1)
            ld = json.dumps({"@type": "BlogPosting", "headline": html.unescape(h1),
                             "url": f"{SITE}/{ARTICLES}/{slug}/", "datePublished": (pub or last).isoformat()},
                            ensure_ascii=False, separators=(",", ":"))
            idx = idx.replace('"blogPost":[\n', '"blogPost":[\n' + ld + ",\n", 1)
            added.append(slug)
    if added:
        open(idx_path, "w", encoding="utf-8").write(idx)
        print("добавлены в список статей:", ", ".join(added))
        newest = max(d for _, d in arts)
        urls = [(u, max(d, newest) if u == f"{SITE}/{ARTICLES}/" else d) for u, d in urls]

    body = "".join(f"  <url><loc>{u}</loc><lastmod>{d.isoformat()}</lastmod></url>\n" for u, d in urls + arts)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "</urlset>\n")
    open(os.path.join(out, "sitemap-all.xml"), "w", encoding="utf-8").write(xml)
    print(f"sitemap-all.xml: {len(urls) + len(arts)} адресов")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
