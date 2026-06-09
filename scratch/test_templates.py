import os
import json
import datetime
from jinja2 import Environment, BaseLoader, TemplateSyntaxError, UndefinedError

# Custom filters
def filter_currency(value, symbol="$"):
    try:
        return f"{symbol}{float(value):,.2f}"
    except (ValueError, TypeError):
        return value

def filter_date(value, format_str="%B %d, %Y"):
    try:
        if isinstance(value, str):
            for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y"):
                try:
                    dt = datetime.datetime.strptime(value, fmt)
                    return dt.strftime(format_str)
                except ValueError:
                    continue
            return value
        elif isinstance(value, (int, float)):
            dt = datetime.datetime.fromtimestamp(value)
            return dt.strftime(format_str)
        return value
    except Exception:
        return value

def filter_mask(value, mask_type="email"):
    try:
        val_str = str(value)
        if mask_type == "email" and "@" in val_str:
            name, domain = val_str.split("@", 1)
            if len(name) <= 2:
                return f"{name[0]}*@{domain}"
            return f"{name[0]}{'*' * (len(name) - 2)}{name[-1]}@{domain}"
        elif mask_type == "card":
            clean_val = "".join(c for c in val_str if c.isdigit())
            if len(clean_val) >= 4:
                return f"{'*' * (len(clean_val) - 4)}{clean_val[-4:]}"
        return val_str
    except Exception:
        return value

def filter_slugify(value):
    import re
    value = str(value).lower()
    value = re.sub(r"[^\w\s-]", "", value)
    return re.sub(r"[-\s]+", "-", value).strip("-")

# Setup Jinja environment
env = Environment(loader=BaseLoader(), autoescape=True)
env.filters["currency"] = filter_currency
env.filters["date"] = filter_date
env.filters["mask"] = filter_mask
env.filters["slugify"] = filter_slugify

CWD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VARIABLES_FILE = os.path.join(CWD, "variables.json")

def test_render():
    with open(VARIABLES_FILE, "r", encoding="utf-8") as f:
        variables = json.load(f)

    # Test template.html.j2 at root
    templates_to_test = [
        ("Default (Root)", os.path.join(CWD, "template.html.j2")),
        ("Modern", os.path.join(CWD, "templates", "modern.html.j2")),
        ("Elegant", os.path.join(CWD, "templates", "elegant.html.j2")),
        ("Professional", os.path.join(CWD, "templates", "professional.html.j2")),
    ]

    for name, path in templates_to_test:
        print(f"Testing template: {name} ({path})")
        if not os.path.exists(path):
            print(f"  [ERROR] File does not exist!")
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                template_str = f.read()
            template = env.from_string(template_str)
            rendered = template.render(**variables)
            print(f"  [SUCCESS] Rendered successfully! Length: {len(rendered)} characters.")
        except Exception as e:
            print(f"  [FAILURE] Error rendering: {str(e)}")

if __name__ == "__main__":
    test_render()
