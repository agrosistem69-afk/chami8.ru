"""After a push to main: tell search engines about new or changed pages (IndexNow)
and, if Telegram secrets are set, post new articles to the channel."""
import json, os, re, subprocess, sys, time, urllib.request, urllib.error, html

SITE = "https://chami8.ru"
KEY = os.environ["INDEXNOW_KEY"]


def locs(text):
    return dict(re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]*)</lastmod>", text))


def old_sitemap():
    before = os.environ.get("BEFORE", "")
    if not before or set(before) == {"0"}:
        return ""
    try:
        return subprocess.check_output(["git", "show", f"{before}:sitemap.xml"], text=True)
    except subprocess.CalledProcessError:
        return ""


def post(url, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(url.split("/bot")[0], r.status)
            return r.read()
    except urllib.error.HTTPError as e:  # keep going: one failed ping must not stop the rest
        print(url.split("/bot")[0], "failed:", e.code, e.read().decode(errors="replace")[:300])
    except Exception as e:
        print(url.split("/bot")[0], "failed:", e)


now, was = locs(open("sitemap.xml", encoding="utf-8").read()), locs(old_sitemap())
if os.environ.get("TEST"):
    # manual run: re-announce the newest article so the Telegram setup can be checked
    arts = [u for u in now if "/articles/" in u and not u.rstrip("/").endswith("/articles")]
    newest = max(arts, key=lambda u: now[u]) if arts else None
    was = {u: d for u, d in now.items() if u != newest}
    os.environ["WAIT"] = "0"
changed = [u for u, d in now.items() if was.get(u) != d]
new = [u for u in now if u not in was]
print("changed:", changed, "new:", new)
if not changed:
    sys.exit(0)

time.sleep(int(os.environ.get("WAIT", "120")))  # let GitHub Pages finish deploying

body = {"host": "chami8.ru", "key": KEY, "keyLocation": f"{SITE}/{KEY}.txt", "urlList": changed}
for endpoint in ("https://yandex.com/indexnow", "https://api.indexnow.org/indexnow"):
    post(endpoint, body)

token, chat = os.environ.get("TG_TOKEN"), os.environ.get("TG_CHAT")
if not (token and chat):
    print("Telegram secrets not set, skipping posts")
    sys.exit(1 if os.environ.get("TEST") else 0)
tg_failed = False
# accept "@name", "name", "t.me/name" or "https://t.me/name"; numeric ids stay as they are
chat = re.sub(r"^(https?://)?(t\.me|telegram\.me)/", "", chat.strip()).strip("/")
if not re.fullmatch(r"-?\d+", chat) and not chat.startswith("@"):
    chat = "@" + chat
print("Telegram chat:", chat)
for u in new:
    if "/articles/" not in u or u.rstrip("/").endswith("/articles"):
        continue
    path = u.replace(SITE, "").strip("/") + "/index.html"
    if not os.path.exists(path):
        continue
    page = open(path, encoding="utf-8").read()
    title = re.search(r"<h1[^>]*>(.*?)</h1>", page, re.S)
    desc = re.search(r'<meta name="description" content="([^"]*)"', page)
    title = re.sub("<[^>]+>", "", title.group(1)).strip() if title else u
    tag_list = re.search(r'<ul class="tags".*?</ul>', page, re.S)
    tags = " ".join(re.findall(r"<li>(#[^<]+)</li>", tag_list.group(0))) if tag_list else ""
    link = f'<a href="{u}">Читать статью целиком на сайте «Ча Ми»</a>'
    story = re.search(r'<template id="tg-post">(.*?)</template>', page, re.S)
    if story:
        # the article's own Telegram text (Telegram HTML: <b>, <i>, <a>, line breaks)
        body_text = re.sub(r"\n[ \t]+", "\n", story.group(1).strip())
        text = f"{body_text}\n\n👉 {link}"
    else:
        text = f"🍵 <b>{html.escape(html.unescape(title))}</b>\n\n{html.escape(html.unescape(desc.group(1))) if desc else ''}\n\n{link}"
    if tags:
        text += f"\n\n{tags}"
    res = post(f"https://api.telegram.org/bot{token}/sendMessage", {"chat_id": chat, "text": text[:4096], "parse_mode": "HTML"})
    if res is None:
        tg_failed = True
        continue
    print("Telegram: posted", u)
    if os.environ.get("TEST"):
        continue  # a test re-post must not move the comments to a new post
    try:
        msg_id = json.loads(res)["result"]["message_id"]
        slug = u.rstrip("/").rsplit("/", 1)[-1]
        posts_file = "articles/tg-posts.json"
        posts = json.load(open(posts_file, encoding="utf-8")) if os.path.exists(posts_file) else {}
        posts[slug] = msg_id
        with open(posts_file, "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
            f.write("\n")
    except Exception as e:
        print("could not save Telegram post id:", e)
sys.exit(1 if tg_failed else 0)
