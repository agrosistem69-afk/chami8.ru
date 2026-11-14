#!/usr/bin/env python3
"""Черновики статей «Ча Ми»: сборка и выпуск.

Черновики лежат в ветке `drafts` (её GitHub Pages не показывает):
  queue.txt           — очередь выпуска, по строке на статью: `slug` или `slug | not_before=ГГГГ-ММ-ДД`
  src/<slug>.html     — исходник статьи: JSON-шапка между `---json` и `---`, затем тело статьи,
                        затем `===TG===` и текст поста для Telegram.

Команды (запускать из корня репозитория, ветка main):
  python3 .github/scripts/drafts.py next [--date ГГГГ-ММ-ДД]      — какая статья выйдет следующей
  python3 .github/scripts/drafts.py publish [--date ...] [--slug S] — выпустить статью в main (без коммита)
  python3 .github/scripts/drafts.py build SRC OUT [--date ...]     — собрать страницу для проверки
  python3 .github/scripts/drafts.py check SRC...                    — проверить исходники
Источник черновиков: ветка origin/drafts (git fetch origin drafts) или папка, заданная DRAFTS_DIR.
"""
import datetime, html, json, os, re, subprocess, sys, urllib.parse

SITE = "https://chami8.ru"
CSS_V, SEASON_V, FU_V, COMMENTS_V = "6", "1", "9", "1"
MONTHS = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа",
          "сентября", "октября", "ноября", "декабря"]

PRODUCTS = {
    "dhp": dict(
        name="Да Хун Пао", zh="大红袍", full="Да Хун Пао 大红袍, 100 г", short="Да Хун Пао, 100 г", price="550",
        img="/articles/img/products/da-hong-pao-100g.webp", w=800, h=1000,
        line="Фуцзяньский улун первого сорта · Zhong Min Hong Tai · хватает примерно на 15–20 чаепитий в гайвани",
        desc="Фуцзяньский улун Да Хун Пао, первый сорт, 100 г. Производитель — кооператив Zhong Min Hong Tai (中闽弘泰), уезд Аньси, Цюаньчжоу, провинция Фуцзянь.",
        brand=True, country="CN", weight=100, h3="Да Хун Пао <span class=\"zh\" lang=\"zh\">大红袍</span>, 100 г"),
    "pu": dict(
        name="пуэр в мандарине", zh="小青柑", full="Пуэр в мандарине 小青柑, 1 шт.", short="Пуэр в мандарине, 1 шт.", price="150",
        img="/articles/img/products/puer-v-mandarine.webp", w=800, h=1000,
        line="Пуэр, высушенный в кожуре мандарина · Zhong Min Hong Tai · один шарик — одно чаепитие на несколько проливов",
        desc="Пуэр в кожуре мандарина (сяо цин гань), продаётся поштучно. Производитель — кооператив Zhong Min Hong Tai (中闽弘泰).",
        brand=True, country="CN", weight=None, h3="Пуэр в мандарине <span class=\"zh\" lang=\"zh\">小青柑</span>, 1 шт."),
    "tgy": dict(
        name="Те Гуань Инь", zh="铁观音", full="Те Гуань Инь 铁观音, пакетик 7 г", short="Те Гуань Инь, 7 г", price="150",
        img="/articles/img/te-guan-in-placeholder.svg", w=800, h=600,
        line="Светлый улун из уезда Аньси · Zhong Min Hong Tai · вакуумный пакетик на одно чаепитие",
        desc="Светлый (ароматный) улун Те Гуань Инь в вакуумном пакетике 7 г. Производитель — кооператив Zhong Min Hong Tai (中闽弘泰), уезд Аньси, провинция Фуцзянь.",
        brand=True, country="CN", weight=7, h3="Те Гуань Инь <span class=\"zh\" lang=\"zh\">铁观音</span>, пакетик 7 г"),
    "honey-raz": dict(
        name="мёд разнотравье", zh="", full="Мёд разнотравье, Липецкая область, 0,4 л", short="Мёд разнотравье, 0,4 л", price="470",
        img="/articles/img/products/myod-raznotrave.svg", w=800, h=1000,
        line="С пасек Липецкой области · полифлорный, с луговых трав · к чаю вприкуску",
        desc="Натуральный мёд разнотравье с пасек Липецкой области, банка 0,4 л.",
        brand=False, country="RU", weight=None, h3="Мёд разнотравье, 0,4 л"),
}
BTN = {"dhp": "Купить Да Хун Пао", "pu": "Купить пуэр в мандарине", "tgy": "Купить Те Гуань Инь", "honey-raz": "Купить мёд"}

METRIKA = """<!-- Yandex.Metrika counter -->
<script type="text/javascript">
    (function(m,e,t,r,i,k,a){
        m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
        m[i].l=1*new Date();
        for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
        k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)
    })(window, document,'script','https://mc.yandex.ru/metrika/tag.js?id=114134559', 'ym');

    ym(114134559, 'init', {ssr:true, webvisor:true, clickmap:true, ecommerce:"dataLayer", referrer: document.referrer, url: location.href, accurateTrackBounce:true, trackLinks:true});
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/114134559" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
<!-- /Yandex.Metrika counter -->"""

STICKY_JS = """<script>
(function(){
  var bar=document.getElementById('stickyBuy'), shop=document.querySelector('.shop'), h1=document.querySelector('h1');
  if(!bar) return; document.body.classList.add('has-sticky');
  var shopOn=false, pastTop=false, upd=function(){ var on=pastTop && !shopOn; bar.classList.toggle('on', on); document.body.classList.toggle('sticky-on', on); };
  if('IntersectionObserver' in window){
    if(shop) new IntersectionObserver(function(e){ shopOn=e[0].isIntersecting; upd(); }).observe(shop);
    if(h1) new IntersectionObserver(function(e){ pastTop=!e[0].isIntersecting && e[0].boundingClientRect.top<0; upd(); }).observe(h1);
  } else { bar.classList.add('on'); }
})();
</script>"""

FOOTER = """<footer><div class="in">
  <span>Ча Ми 茶蜜 · китайский чай и липецкий мёд</span>
  <a href="/#offer">Оферта</a><a href="/#privacy">Политика конфиденциальности</a><a href="/#delivery">Доставка и возврат</a><a href="https://t.me/chami8ru" target="_blank" rel="noopener">Telegram</a>
  <span>© {year} · ИП Кордеро Гонсалес Г. Д. · ИНН 771977151064</span>
</div></footer>"""

REQUIRED = ["slug", "title", "description", "h1", "crumb", "keywords", "product", "card", "llms",
            "faq", "sources", "tags", "cta"]


def ru_date(d):
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def parse_src(text):
    m = re.match(r"\s*---json\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not m:
        raise ValueError("нет JSON-шапки ---json … ---")
    meta = json.loads(m.group(1))
    rest = m.group(2)
    if "===TG===" not in rest:
        raise ValueError("нет раздела ===TG===")
    body, tg = rest.split("===TG===", 1)
    return meta, body.strip(), tg.strip()


def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s)


def words(s):
    return len(re.findall(r"[\wёЁ-]+", strip_tags(s)))


def check(meta, body, tg, path=""):
    errs = []
    for k in REQUIRED:
        if k not in meta:
            errs.append(f"нет поля {k}")
    if errs:
        return errs
    if len(full_title(meta)) > 65:
        errs.append(f"title {len(full_title(meta))} > 65 знаков")
    if len(meta["description"]) > 160:
        errs.append(f"description {len(meta['description'])} > 160 знаков")
    if meta["product"] not in PRODUCTS:
        errs.append("неизвестный product")
    n = words(body)
    if n < 1100:
        errs.append(f"мало слов в теле: {n}")
    t = len(strip_tags(tg))
    if not 1500 <= t <= 2600:
        errs.append(f"пост Telegram {t} знаков (нужно 1500–2500)")
    if not meta["tags"] or meta["tags"][-1] != "#ЧаМи":
        errs.append("последний хештег должен быть #ЧаМи")
    if not 4 <= len(meta["faq"]) <= 7:
        errs.append("в FAQ нужно 4–6 вопросов")
    if not 3 <= len(meta["sources"]) <= 7:
        errs.append("источников нужно 3–6")
    if 'class="tldr"' not in body:
        errs.append("нет блока «Коротко» (div.tldr)")
    for img in re.findall(r'src="(/articles/img/[^"]+)"', body):
        if not os.path.exists(img.lstrip("/")):
            errs.append(f"нет файла {img}")
    if re.search(r"<(script|style)", body, re.I):
        errs.append("в теле нельзя script/style")
    bad = re.sub(r"</?(b|i|a)( href=\"[^\"]+\")?>", "", tg)
    if "<" in bad:
        errs.append("в посте Telegram только <b>, <i>, <a href>")
    return errs


def full_title(meta):
    t = meta["title"]
    return t + " | Ча Ми" if len(t) + 8 <= 65 else t


def cjk_text(s):
    chars = sorted(set(ch for ch in s if "㐀" <= ch <= "鿿"))
    return urllib.parse.quote("".join(chars))


def first_img(body):
    m = re.search(r'<img src="([^"]+)" width="(\d+)" height="(\d+)"[^>]*alt="([^"]*)"', body)
    if m:
        return m.group(1), int(m.group(2)), int(m.group(3)), m.group(4)
    return "/articles/img/photos/skala-pialy-nastoj.webp", 750, 1000, "Пиалы с настоем чая на камне"


def unlink_missing(s, published):
    """Ссылки на ещё не вышедшие статьи: в списках убираем пункт, в тексте оставляем только слова."""
    def ok(slug):
        return slug in published
    s = re.sub(r'\s*<li><a href="/articles/([a-z0-9-]+)/">[^<]*</a>[^<]*</li>',
               lambda m: m.group(0) if ok(m.group(1)) else "", s)
    s = re.sub(r'<a href="/articles/([a-z0-9-]+)/(#[^"]*)?">(.*?)</a>',
               lambda m: m.group(0) if ok(m.group(1)) else m.group(3), s)
    return s


def build(meta, body, tg, date, published=None, modified=None):
    d = datetime.date.fromisoformat(date)
    modified = modified or date
    slug = meta["slug"]
    url = f"{SITE}/articles/{slug}/"
    p = PRODUCTS[meta["product"]]
    pid = meta["product"]
    og_src, _, _, _ = first_img(body)
    og = meta.get("og_image", og_src)
    minutes = max(4, round(words(body) / 180))
    faq = meta["faq"]
    esc = html.escape

    product_ld = {"@type": "Product", "@id": url + "#product", "name": p["full"], "description": p["desc"],
                  "image": SITE + p["img"]}
    if p["brand"]:
        product_ld["brand"] = {"@type": "Brand", "name": "Zhong Min Hong Tai"}
    product_ld["countryOfOrigin"] = p["country"]
    if p["weight"]:
        product_ld["weight"] = {"@type": "QuantitativeValue", "value": p["weight"], "unitCode": "GRM"}
    product_ld["offers"] = {"@type": "Offer", "price": p["price"], "priceCurrency": "RUB",
                            "availability": "https://schema.org/InStock", "url": f"{SITE}/?add={pid}",
                            "seller": {"@type": "Organization", "name": "Ча Ми 茶蜜"}}
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BlogPosting", "@id": url + "#article", "headline": meta["h1"], "description": meta["description"],
         "inLanguage": "ru", "datePublished": date, "dateModified": modified, "mainEntityOfPage": url,
         "image": SITE + og,
         "author": {"@type": "Person", "name": "Грегорио Кордеро", "jobTitle": "основатель магазина «Ча Ми»", "url": SITE + "/"},
         "publisher": {"@type": "Organization", "name": "Ча Ми 茶蜜", "url": SITE + "/"},
         "about": {"@id": url + "#product"}, "keywords": meta["keywords"]},
        product_ld,
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Ча Ми", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Статьи о чае", "item": SITE + "/articles/"},
            {"@type": "ListItem", "position": 3, "name": meta["crumb"], "item": url}]},
        {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in faq]},
    ]}

    faq_html = "\n".join(f"  <dt>{q}</dt>\n  <dd>{a}</dd>" for q, a in faq)
    related = meta.get("related", [])
    rel_items = "".join(f'<li><a href="/articles/{s}/">{t}</a></li>' for s, t in related)
    rel_items += '<li><a href="/articles/">Все статьи о чае и мёде</a></li>'
    src_items = "\n".join(
        f'    <li><a href="{esc(u, quote=True)}" target="_blank" rel="noopener">{t}</a>{(" (" + l + ")") if l else ""}</li>'
        for u, t, l in meta["sources"])
    tags = "".join(f"<li>{t}</li>" for t in meta["tags"])
    shop_img_alt = p["full"] + (", Zhong Min Hong Tai" if p["brand"] else "")

    page_body = f"""<article>
<h1>{meta['h1']}</h1>
<p class="meta">Грегорио Кордеро, основатель «Ча Ми» · <time datetime="{date}">{ru_date(d)}</time> · {minutes} минут чтения</p>

{body}

<section class="shop" aria-label="{BTN[pid]}">
  <img src="{p['img']}" width="{p['w']}" height="{p['h']}" loading="lazy" alt="{shop_img_alt}">
  <div>
    <h3>{p['h3']}</h3>
    <p>{meta.get('shop_line', p['line'])}</p>
    <div class="price">{p['price']} ₽</div>
    <a class="btn" href="/?add={pid}">{BTN[pid]}</a>
    <p>Доставка оплачивается отдельно. Отправляем в течение 3 рабочих дней.</p>
  </div>
</section>

<h2>Вопросы и ответы</h2>
<dl class="faq">
{faq_html}
</dl>

<p class="cta-end">{meta['cta']}</p>

<div class="more">
  <p>Читайте также</p>
  <ul>{rel_items}</ul>
</div>

<div class="more">
  <p>Источники</p>
  <ul>
{src_items}
  </ul>
</div>
{meta.get('after_sources', '')}
<template id="tg-post">
{tg}
</template>

<ul class="tags" aria-label="Хештеги">{tags}</ul>

<section class="comments" id="comments" aria-label="Комментарии">
  <h2>Комментарии</h2>
</section>
</article>"""
    if published is not None:
        page_body = unlink_missing(page_body, published)

    footer = FOOTER.format(year=d.year)
    sticky = f"""<div class="sticky-buy" id="stickyBuy" aria-label="{BTN[pid]}">
  <div class="in">
    <img src="{p['img']}" width="44" height="55" alt="{p['short']}">
    <span class="nm">{p['short']}<b>{p['price']} ₽</b></span>
    <a class="btn" href="/?add={pid}">Купить</a>
  </div>
</div>"""
    header = """<header class="top"><div class="in">
  <a class="brand" href="/"><span class="seal" aria-hidden="true">茶蜜</span><b>Ча Ми</b></a>
  <nav aria-label="Меню"><a href="/#tea">Чай</a><a href="/#honey">Мёд</a><a href="/articles/">Статьи</a><a href="/#cart">Корзина</a></nav>
</div></header>"""
    crumbs = f'<nav class="crumbs" aria-label="Навигация"><a href="/">Ча Ми</a> › <a href="/articles/">Статьи о чае</a> › {meta["crumb"]}</nav>'
    fonts_text = cjk_text(page_body + header + footer)
    og_title = meta.get("og_title", meta["h1"])
    head = f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title(meta)}</title>
<meta name="description" content="{esc(meta['description'], quote=True)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="article">
<meta property="og:locale" content="ru_RU">
<meta property="og:site_name" content="Ча Ми 茶蜜">
<meta property="og:title" content="{esc(og_title, quote=True)}">
<meta property="og:description" content="{esc(meta['description'], quote=True)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{og}">
<meta property="article:published_time" content="{date}">
<meta property="article:modified_time" content="{modified}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&family=Alegreya:wght@400;500;700&display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&display=swap&text={fonts_text}">
<link rel="stylesheet" href="/articles/article.css?v={CSS_V}">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False)}
</script>
{METRIKA}
</head>
<body>
{header}

{crumbs}

{page_body}

{footer}
{sticky}
{STICKY_JS}
<script src="/season.js?v={SEASON_V}" defer></script>
<script src="/fu.js?v={FU_V}" defer></script>
<script src="/articles/comments.js?v={COMMENTS_V}" defer></script>
</body>
</html>
"""
    return head


# ---------- выпуск ----------

def drafts_read(path):
    base = os.environ.get("DRAFTS_DIR")
    if base:
        with open(os.path.join(base, path), encoding="utf-8") as f:
            return f.read()
    return subprocess.run(["git", "show", f"origin/drafts:{path}"], check=True, capture_output=True,
                          text=True).stdout


def published_slugs():
    return {n for n in os.listdir("articles") if os.path.isfile(f"articles/{n}/index.html")}


def queue():
    out = []
    for line in drafts_read("queue.txt").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        parts = [x.strip() for x in line.split("|")]
        opts = dict(x.split("=", 1) for x in parts[1:] if "=" in x)
        out.append((parts[0], opts))
    return out


def next_slug(date):
    pub = published_slugs()
    for slug, opts in queue():
        if slug in pub:
            continue
        nb = opts.get("not_before")
        if nb and date < nb:
            continue
        try:
            drafts_read(f"src/{slug}.html")
        except Exception:
            continue
        return slug
    return None


def publish(slug, date):
    meta, body, tg = parse_src(drafts_read(f"src/{slug}.html"))
    errs = check(meta, body, tg)
    if errs:
        sys.exit("Черновик не прошёл проверку: " + "; ".join(errs))
    pub = published_slugs() | {slug}
    page = build(meta, body, tg, date, published=pub)
    os.makedirs(f"articles/{slug}", exist_ok=True)
    with open(f"articles/{slug}/index.html", "w", encoding="utf-8") as f:
        f.write(page)
    d = datetime.date.fromisoformat(date)
    url = f"{SITE}/articles/{slug}/"

    # карточка и JSON-LD в списке статей
    idx = open("articles/index.html", encoding="utf-8").read()
    if f'href="/articles/{slug}/"' not in idx:
        src, w, h, alt = first_img(body)
        card = f"""<!--POSTS-->
  <li>
    <img src="{src}" width="{w}" height="{h}" loading="lazy" alt="{alt}">
    <div class="tx">
      <h2><a href="/articles/{slug}/">{meta['h1']}</a></h2>
      <p>{meta['card']}</p>
      <p class="meta"><time datetime="{date}">{ru_date(d)}</time></p>
    </div>
  </li>"""
        idx = idx.replace("<!--POSTS-->", card, 1)
        ld = json.dumps({"@type": "BlogPosting", "headline": meta["h1"], "url": url, "datePublished": date},
                        ensure_ascii=False, separators=(",", ":"))
        idx = idx.replace('"blogPost":[\n', '"blogPost":[\n' + ld + ",\n", 1)
        open("articles/index.html", "w", encoding="utf-8").write(idx)

    # sitemap
    sm = open("sitemap.xml", encoding="utf-8").read()
    sm = re.sub(r"(<loc>https://chami8.ru/articles/</loc><lastmod>)[^<]+", r"\g<1>" + date, sm)
    if url not in sm:
        sm = sm.replace("</urlset>", f"  <url><loc>{url}</loc><lastmod>{date}</lastmod></url>\n</urlset>")
    open("sitemap.xml", "w", encoding="utf-8").write(sm)

    # llms.txt
    ll = open("llms.txt", encoding="utf-8").read()
    if url not in ll:
        line = f"- [{meta['h1']}]({url}): {meta['llms']}\n"
        ll = ll.replace("- [Все статьи](https://chami8.ru/articles/)", line + "- [Все статьи](https://chami8.ru/articles/)", 1)
        open("llms.txt", "w", encoding="utf-8").write(ll)

    # отметка в ARTICLES.md
    am = open("ARTICLES.md", encoding="utf-8").read()
    am2 = re.sub(r"^(\|\s*[^|]+\|\s*" + re.escape(slug) + r"\s*\|\s*)(?!✅)",
                 r"\g<1>✅ опубликовано " + date + " — ", am, count=1, flags=re.M)
    open("ARTICLES.md", "w", encoding="utf-8").write(am2)
    print(f"Выпущено: /articles/{slug}/ ({meta['h1']})")
    return meta


def main(argv):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["next", "publish", "build", "check"])
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--slug")
    a = ap.parse_args(argv)
    if a.cmd == "check":
        bad = 0
        for p in a.paths:
            try:
                meta, body, tg = parse_src(open(p, encoding="utf-8").read())
                errs = check(meta, body, tg, p)
                if os.path.basename(p) != meta.get("slug", "") + ".html":
                    errs.append("имя файла не совпадает со slug")
            except Exception as e:
                errs = [str(e)]
            print(("OK   " if not errs else "FAIL ") + p + (": " + "; ".join(errs) if errs else
                  f"  ({words(body)} слов, пост {len(strip_tags(tg))} зн.)"))
            bad += bool(errs)
        sys.exit(1 if bad else 0)
    if a.cmd == "build":
        meta, body, tg = parse_src(open(a.paths[0], encoding="utf-8").read())
        open(a.paths[1], "w", encoding="utf-8").write(build(meta, body, tg, a.date, published=published_slugs() | {meta['slug']}))
        return
    slug = a.slug or next_slug(a.date)
    if a.cmd == "next":
        print(slug or "НЕТ ГОТОВЫХ ЧЕРНОВИКОВ")
        return
    if not slug:
        sys.exit("Нет готовых черновиков для выпуска")
    publish(slug, a.date)


if __name__ == "__main__":
    main(sys.argv[1:])
