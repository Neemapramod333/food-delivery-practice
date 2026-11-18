# Builds the website: puts the menu into the page template.
import datetime
import json
import os

with open("menu.json", encoding="utf-8") as f:
    menu = json.load(f)
with open("template.html", encoding="utf-8") as f:
    page = f.read()

menu_data = json.dumps(menu).replace("</", "<\\/")
version = os.environ.get("GITHUB_SHA", "local")[:7]
ist = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
built_at = datetime.datetime.now(ist).strftime("%d %b %Y, %I:%M %p IST")

page = page.replace("{{MENU_JSON}}", menu_data)
page = page.replace("{{VERSION}}", version)
page = page.replace("{{BUILT_AT}}", built_at)

os.makedirs("site", exist_ok=True)
with open("site/index.html", "w", encoding="utf-8") as f:
    f.write(page)

print(f"Built site/index.html with {len(menu['items'])} dishes, version {version}, at {built_at}")
