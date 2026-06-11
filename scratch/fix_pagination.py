import os
import re
import glob

CWD = "/home/mustak24/Documents/Coding/Python/RenderJinja2/templates"
files = glob.glob(os.path.join(CWD, "*.html.j2"))

# Including the template.html.j2 just in case
files.append("/home/mustak24/Documents/Coding/Python/RenderJinja2/template.html.j2")

for filepath in files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Apply replacements
    content = re.sub(r'\{% set items_per_page = 24 %\}', '{% set items_per_page = 14 %}', content)
    content = re.sub(r'\{% set hsn_per_page = 12 %\}', '{% set hsn_per_page = 10 %}', content)
    content = re.sub(r'\{% set row_height = 5 %\} {# each row ≈ 5mm #}', '{% set row_height = 8 %} {# each row ≈ 8mm #}', content)
    
    content = re.sub(r'\{% if total_items <= 18 and total_hsn <= 4 %\}', '{% if total_items <= 10 and total_hsn <= 3 %}', content)
    content = re.sub(r'\{% if total_items <= 18 and total_hsn <=4 %\}', '{% if total_items <= 10 and total_hsn <= 3 %}', content)
    
    content = re.sub(r'\{% elif total_items <= 18 and total_hsn > 4 %\}', '{% elif total_items <= 10 and total_hsn > 3 %}', content)
    content = re.sub(r'\{% elif total_items <=18 and total_hsn > 4 %\}', '{% elif total_items <= 10 and total_hsn > 3 %}', content)
    
    content = re.sub(r'\{# ---------- CASE 3: Items 18-24 ---------- #\}', '{# ---------- CASE 3: Items 10-14 ---------- #}', content)
    content = re.sub(r'\{% elif total_items > 18 and total_items <= 24 %\}', '{% elif total_items > 10 and total_items <= 14 %}', content)
    
    content = re.sub(r'\{# ---------- CASE 4: Items > 24 ---------- #\}', '{# ---------- CASE 4: Items > 14 ---------- #}', content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Done")
