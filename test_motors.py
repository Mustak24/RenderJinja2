from jinja2 import Environment, FileSystemLoader
import json

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('templates/motors.html.j2')

# Dummy data for motors template
data = {
    "company": {"company_name": "Test Co", "address_1": "123 Main St", "phone": {"code": "+91", "number": "1234567890"}, "tin": "123"},
    "party": {"name": "Test Party"},
    "invoice": {
        "voucher_number": "INV-01", "date": "2026-01-01",
        "items": [
            {"name": "Item 1", "qty": 1, "rate": 100, "amount": 100, "tax_amount": 10, "total_amount": 110, "hsn": "1234", "pack": "NOS", "discount_amount": 0, "tax_rate": 18}
        ],
        "taxes": [],
        "totals": {"cgst": 0, "sgst": 0},
        "grand_total": 110
    }
}

html = template.render(**data)
with open('scratch/test_motors.html', 'w') as f:
    f.write(html)
print("Rendered motors to scratch/test_motors.html")
