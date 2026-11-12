"""Once a day: take the first article from .github/tg-queue.json, delete its old
Telegram post (if any), post the new story from the article and save the post number
for comments. Used to re-post articles that came out before comments were turned on."""
import json, os, re, sys, urllib.request, urllib.error, html

SITE = "https://chami8.ru"
QUEUE = ".github/tg-queue.json"
POSTS = "articles/tg-posts.json"


def tg(method, payload):
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/{method}", data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(method, "failed:", e.code, e.read().decode(errors="replace")[:300])


token, chat = os.environ["TG_TOKEN"], os.environ["TG_CHAT"]
chat = re.sub(r"^(https?://)?(t\.me|telegram\.me)/", "", chat.strip()).strip("/")
if not re.fullmatch(r"-?\d+", chat) and not chat.startswith("@"):
    chat = "@" + chat

queue = json.load(open(QUEUE, encoding="utf-8"))
if not queue:
    print("queue is empty")
    sys.exit(0)
item = queue[0]
slug = item["slug"]
url = f"{SITE}/articles/{slug}/"
page = open(f"articles/{slug}/index.html", encoding="utf-8").read()
story = re.search(r'<template id="tg-post">(.*?)</template>', page, re.S)
if not story:
    sys.exit(f"{slug}: no <template id=\"tg-post\"> in the article")
tag_list = re.search(r'<ul class="tags".*?</ul>', page, re.S)
tags = " ".join(re.findall(r"<li>(#[^<]+)</li>", tag_list.group(0))) if tag_list else ""
text = re.sub(r"\n[ \t]+", "\n", story.group(1).strip()) + f'\n\n👉 <a href="{url}">Читать статью целиком на сайте «Ча Ми»</a>'
if tags:
    text += f"\n\n{tags}"

res = tg("sendMessage", {"chat_id": chat, "text": text[:4096], "parse_mode": "HTML"})
if not res or not res.get("ok"):
    sys.exit("could not post " + slug)
msg_id = res["result"]["message_id"]
print("posted", slug, "as", msg_id)

posts = json.load(open(POSTS, encoding="utf-8")) if os.path.exists(POSTS) else {}
posts[slug] = msg_id
with open(POSTS, "w", encoding="utf-8") as f:
    json.dump(posts, f, ensure_ascii=False, indent=2)
    f.write("\n")

if item.get("delete"):
    d = tg("deleteMessage", {"chat_id": chat, "message_id": item["delete"]})
    if d and d.get("ok"):
        print("deleted old post", item["delete"])
    else:
        # Telegram lets bots delete only fresh posts; an older one has to be deleted by hand
        print(f"::warning::old post {item['delete']} was not deleted, delete it by hand: https://t.me/{chat.lstrip('@')}/{item['delete']}")

with open(QUEUE, "w", encoding="utf-8") as f:
    json.dump(queue[1:], f, ensure_ascii=False, indent=2)
    f.write("\n")
