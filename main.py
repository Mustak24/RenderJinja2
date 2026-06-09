import os
import asyncio
import json
import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from jinja2 import Environment, BaseLoader, TemplateSyntaxError, UndefinedError

app = FastAPI(title="Jinja2 Live Preview & Sandbox")

# Custom Jinja2 Environment with BaseLoader
env = Environment(loader=BaseLoader(), autoescape=True)

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

env.filters["currency"] = filter_currency
env.filters["date"] = filter_date
env.filters["mask"] = filter_mask
env.filters["slugify"] = filter_slugify

# Paths for files to watch
CWD = os.getcwd()
VARIABLES_FILE = os.path.join(CWD, "variables.json")

def load_and_render(template_filename="template.html.j2"):
    if template_filename == "template.html.j2":
        template_path = os.path.join(CWD, "template.html.j2")
    else:
        template_path = os.path.join(CWD, "templates", template_filename)

    if not os.path.exists(template_path):
        return {
            "success": False,
            "error_type": "FileNotFoundError",
            "message": f"'{template_path}' not found.\nPlease make sure the file exists."
        }
    if not os.path.exists(VARIABLES_FILE):
        return {
            "success": False,
            "error_type": "FileNotFoundError",
            "message": f"'{VARIABLES_FILE}' not found in project root.\nPlease create this file in VS Code."
        }

    # Read template file
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template_str = f.read()
    except Exception as e:
        return {"success": False, "error_type": "ReadError", "message": f"Failed to read template file:\n{str(e)}"}

    # Read variables file
    try:
        with open(VARIABLES_FILE, "r", encoding="utf-8") as f:
            vars_str = f.read()
        variables = json.loads(vars_str)
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error_type": "JSONDecodeError",
            "message": f"JSON Syntax Error in 'variables.json':\n{str(e)}"
        }
    except Exception as e:
        return {"success": False, "error_type": "ReadError", "message": f"Failed to read variables file:\n{str(e)}"}

    # Render with Jinja2
    try:
        template = env.from_string(template_str)
        rendered_html = template.render(**variables)
        return {"success": True, "rendered": rendered_html}
    except TemplateSyntaxError as e:
        return {
            "success": False,
            "error_type": "TemplateSyntaxError",
            "message": f"Line {e.lineno}: {e.message}",
            "line": e.lineno
        }
    except UndefinedError as e:
        return {
            "success": False,
            "error_type": "UndefinedError",
            "message": f"Undefined variable: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error_type": "RenderError",
            "message": f"Error during rendering:\n{str(e)}"
        }


@app.get("/", response_class=HTMLResponse)
async def get_index():
    index_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h3>Error: templates/index.html not found!</h3>"


@app.get("/api/templates")
async def get_templates():
    templates = []
    # Check default root template
    if os.path.exists(os.path.join(CWD, "template.html.j2")):
        templates.append({"name": "Default (Root)", "filename": "template.html.j2"})
    # Check templates folder for other templates
    templates_dir = os.path.join(CWD, "templates")
    if os.path.exists(templates_dir):
        for filename in sorted(os.listdir(templates_dir)):
            if filename.endswith(".html.j2"):
                name = filename.replace(".html.j2", "").replace("_", " ").title()
                templates.append({"name": name, "filename": filename})
    return templates


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Get template filename from query param
    template_filename = websocket.query_params.get("template", "template.html.j2")
    if template_filename == "template.html.j2":
        template_path = os.path.join(CWD, "template.html.j2")
    else:
        template_path = os.path.join(CWD, "templates", template_filename)

    last_template_mtime = 0.0
    last_vars_mtime = 0.0

    try:
        while True:
            t_changed = False
            v_changed = False

            if os.path.exists(template_path):
                t_mtime = os.path.getmtime(template_path)
                if t_mtime != last_template_mtime:
                    last_template_mtime = t_mtime
                    t_changed = True

            if os.path.exists(VARIABLES_FILE):
                v_mtime = os.path.getmtime(VARIABLES_FILE)
                if v_mtime != last_vars_mtime:
                    last_vars_mtime = v_mtime
                    v_changed = True

            if t_changed or v_changed:
                result = load_and_render(template_filename)
                await websocket.send_json(result)

            await asyncio.sleep(0.3)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WebSocket closed with error: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
