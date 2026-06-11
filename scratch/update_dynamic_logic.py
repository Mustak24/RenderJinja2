import os
import glob
import re

CWD = "/home/mustak24/Documents/Coding/Python/RenderJinja2/templates"
files = glob.glob(os.path.join(CWD, "*.html.j2"))
files.append("/home/mustak24/Documents/Coding/Python/RenderJinja2/template.html.j2")

dynamic_logic = """    {# ---------------- PAGE LOGIC ---------------- #}
    {% set total_items = invoice["items"]|length %}
    {% set total_hsn = invoice["taxes"]|length %}
    
    {# Configure row heights dynamically. Modify these if template padding changes. #}
    {% set row_height = 8 %} {# each item row ≈ 8mm #}
    {% set hsn_row_height = 6 %} {# each HSN row ≈ 6mm #}
    {% set items_header_height = 12 %} {# height of items table header ≈ 12mm #}
    {% set totals_base_height = 65 %} {# base height of totals section without HSN ≈ 65mm #}
    {% set page_body_height = 140 %} {# space between header & footer in mm #}
    
    {# Dynamically calculate max items and HSN per full page #}
    {% set items_per_page = ((page_body_height - items_header_height) // row_height) | int %}
    {% set hsn_per_page = ((page_body_height - totals_base_height) // hsn_row_height) | int %}
    
    {# Calculate total pages needed for items #}
    {% set items_pages = (total_items // items_per_page) + (1 if total_items % items_per_page > 0 else 0) %}
    {% if items_pages == 0 %}{% set items_pages = 1 %}{% endif %}
    
    {% set taxes_total_height = totals_base_height + (total_hsn * hsn_row_height) %}
    
    {% for page in range(items_pages) %}
        {% set start = page * items_per_page %}
        {% set end = start + items_per_page %}
        {% set page_items = invoice["items"][start:end] %}
        
        {{ invoice_header() }}
        {{ items_table(page_items, offset=start) }}
        
        {% if loop.last %}
            {# We are on the last items page. Check if totals fit here. #}
            {% set space_used_by_items = items_header_height + (page_items|length * row_height) %}
            {% set remaining_space = page_body_height - space_used_by_items %}
            
            {% if remaining_space >= taxes_total_height %}
                {# Totals fit on this page completely #}
                {{ totals_section(invoice["taxes"], last_page=True) }}
                {{ fill_space(remaining_space - taxes_total_height) }}
                {{ invoice_footer() }}
            {% else %}
                {# Totals do not fit. Fill space, page break, and render totals on new page(s) #}
                {{ fill_space(remaining_space, text='Continued on next page...') }}
                {{ invoice_footer() }}
                
                {% set hsn_pages = (total_hsn // hsn_per_page) + (1 if total_hsn % hsn_per_page > 0 else 0) %}
                {% if hsn_pages == 0 %}{% set hsn_pages = 1 %}{% endif %}
                
                {% for p in range(hsn_pages) %}
                    <div style="page-break-after: always !important;"></div>
                    {{ invoice_header() }}
                    
                    {% set hstart = p * hsn_per_page %}
                    {% set hend = hstart + hsn_per_page %}
                    {% set hsn_chunk = invoice["taxes"][hstart:hend] %}
                    
                    {{ totals_section(hsn_chunk, last_page=loop.last) }}
                    
                    {% set hsn_space_used = totals_base_height + (hsn_chunk|length * hsn_row_height) %}
                    {{ fill_space(page_body_height - hsn_space_used) }}
                    {{ invoice_footer() }}
                {% endfor %}
            {% endif %}
            
        {% else %}
            {# Not the last items page #}
            {% set space_used_by_items = items_header_height + (page_items|length * row_height) %}
            {{ fill_space(page_body_height - space_used_by_items, text='Continued on next page...') }}
            {{ invoice_footer() }}
            <div style="page-break-after: always !important;"></div>
        {% endif %}
    {% endfor %}
"""

for filepath in files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # We find the index of {# ---------------- PAGE LOGIC ---------------- #}
    match = re.search(r'\{\# -+ PAGE LOGIC -+ \#\}', content)
    if not match:
        print(f"Skipping {filepath}, PAGE LOGIC not found.")
        continue
    
    start_idx = match.start()
    
    # We find the end of the file or the body close tag
    end_idx = content.find("</body>", start_idx)
    if end_idx == -1:
        # Check if there is an ending div to keep
        end_idx = len(content)
        print(f"Warning: </body> not found in {filepath}")
    else:
        # Also let's check if there's a div closing before body that we shouldn't overwrite 
        # In modern.html.j2 there is:
        #     {% endif %}
        #     </div>
        # </body>
        # So we should find the last {% endif %} and replace everything up to it.
        pass

    # A better regex: match from PAGE LOGIC to the last {% endif %}
    pattern = r'\{\# -+ PAGE LOGIC -+ \#\}.*?\{% endif %\}'
    # Wait, there are multiple {% endif %}'s in the original.
    # Actually, let's just replace from PAGE LOGIC up to the first </div> or </body> whichever comes first,
    # wait no, some templates don't have <div class="invoice-container">.
    pass

# Instead of regex, I'll write a function that finds PAGE LOGIC and then 
# removes all lines until the line containing </div> or </body>

for filepath in files:
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    start_idx = -1
    for i, line in enumerate(lines):
        if "{# ---------------- PAGE LOGIC ---------------- #}" in line:
            start_idx = i
            break
            
    if start_idx == -1:
        print(f"PAGE LOGIC not found in {filepath}")
        continue
        
    end_idx = -1
    for i in range(len(lines) - 1, start_idx, -1):
        if "</body>" in lines[i] or "</div>" in lines[i]:
            # Wait, elegant.html.j2 might have a </div> right before </body>.
            # We want to replace everything BETWEEN PAGE LOGIC and the first of (</div>, </body>) 
            # looking forwards from start_idx. Wait, looking forwards, the original code had 
            # <div style="page-break-after: always !important;"></div> inside the logic!
            pass
            
    # Safest way: Look backwards from the end of the file. Find </body>. Then find if there's a </div> right before it.
    end_idx = len(lines) - 1
    for i in range(len(lines) - 1, -1, -1):
        if "</body>" in lines[i]:
            end_idx = i
            break
            
    # Check if the line before </body> is a closing div for invoice-container
    if "</div>" in lines[end_idx - 1]:
        end_idx -= 1
        
    # Replace lines[start_idx:end_idx] with our dynamic logic
    new_lines = lines[:start_idx] + [dynamic_logic + "\n"] + lines[end_idx:]
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
        
    print(f"Updated {filepath}")
