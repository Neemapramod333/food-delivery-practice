# Business rules for the Tiffin Trail menu.
# The pipeline runs this first. If any rule fails, the website is NOT updated.
import json
import sys

ALLOWED_CATEGORIES = ["South Indian", "Starters", "Mains", "Desserts", "Drinks"]
LOWEST_PRICE = 20
HIGHEST_PRICE = 1500

with open("menu.json", encoding="utf-8") as f:
    menu = json.load(f)

problems = []
items = menu["items"]

# Rule 1: every dish has all its details
for item in items:
    for field in ["id", "name", "category", "price", "veg", "desc"]:
        if field not in item:
            problems.append(f"{item.get('name', '?')}: missing '{field}'")

# Rule 2: no two dishes share an id
ids = [item.get("id") for item in items]
for dish_id in set(ids):
    if ids.count(dish_id) > 1:
        problems.append(f"id {dish_id} is used more than once")

# Rule 3: prices are sensible (catches typos like an extra zero)
for item in items:
    price = item.get("price", 0)
    if not (LOWEST_PRICE <= price <= HIGHEST_PRICE):
        problems.append(f"{item.get('name')}: price {price} is outside {LOWEST_PRICE} to {HIGHEST_PRICE}")

# Rule 4: every dish is in a known category
for item in items:
    if item.get("category") not in ALLOWED_CATEGORIES:
        problems.append(f"{item.get('name')}: unknown category '{item.get('category')}'")

# Rule 5: delivery settings make sense
if not (0 <= menu["delivery_fee"] <= 100):
    problems.append(f"delivery fee {menu['delivery_fee']} must be between 0 and 100")
if menu["free_delivery_above"] <= menu["min_order"]:
    problems.append("free delivery amount must be higher than the minimum order")

print(f"Checked {len(items)} dishes against 5 rules.")
if problems:
    for p in problems:
        print("FAIL  " + p)
    print("Menu has problems. The website will NOT be updated.")
    sys.exit(1)

print("PASS  All rules passed. Safe to build and deploy.")
