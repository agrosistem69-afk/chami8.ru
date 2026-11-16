#!/usr/bin/env python3
"""Отправить в IndexNow (Яндекс, Bing) адреса из живой https://chami8.ru/sitemap-all.xml,
у которых lastmod за последние DAYS дней (по Москве). Если карты на сайте ещё нет, выходит без ошибки."""
import datetime, json, os, re, sys, time, urllib.error, urllib.request

HOST = "chami8.ru"
SITE = f"https://{HOST}"
SITEMAP = os.environ.get("SITEMAP_URL", f"{SITE}/sitemap-all.xml")
KEY = os.environ["INDEXNOW_KEY"]
DAYS = int(os.environ.get("DAYS") or 2)
MSK = datetime.timezone(datetime.timedelta(hours=3))
ENDPOINTS = ["https://yandex.com/indexnow", "https://api.indexnow.org/indexnow"]


def fetch(url):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "chami8-indexnow"}), timeout=30) as r:
                return r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            print("карта не скачалась:", e.code)
        except Exception as e:
            print("карта не скачалась:", e)
        time.sleep(10)
    return None


text = fetch(SITEMAP)
if not text or "<urlset" not in text:
    print(f"{SITEMAP} на сайте пока нет — нечего отправлять.")
    sys.exit(0)

since = datetime.datetime.now(MSK).date() - datetime.timedelta(days=DAYS)
urls = [loc for loc, mod in re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>(\d{4}-\d\d-\d\d)", text)
        if datetime.date.fromisoformat(mod) >= since and loc.startswith(SITE)]
print(f"в карте за последние {DAYS} дн. (с {since}): {len(urls)} адресов")
for u in urls:
    print("  ", u)
if not urls:
    sys.exit(0)

body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"{SITE}/{KEY}.txt", "urlList": urls}).encode()
for ep in ENDPOINTS:
    req = urllib.request.Request(ep, data=body, headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"{ep}: отправлено {len(urls)}, ответ {r.status} (200/202 = принято)")
    except urllib.error.HTTPError as e:
        print(f"{ep}: отправлено {len(urls)}, ответ {e.code} {e.read().decode(errors='replace')[:300]}")
    except Exception as e:
        print(f"{ep}: ошибка {e}")
