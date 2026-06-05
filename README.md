# Jinja2 Live Preview & Sandbox

A simple, modern, and high-performance Python application built with **FastAPI** and **Jinja2** to render templates with dynamic variables in real-time. It features a responsive layout with **Monaco Editor** integration (like VS Code), pre-configured templates, customizable viewports, and custom filter support.

## Features

- **Monaco Code Editors**: Write your Jinja2 templates (with HTML/CSS syntax highlighting) and JSON variables (with real-time JSON validation) using the Monaco editor engines from VS Code.
- **Dynamic Live Preview**: Automatically compiles and updates the output preview iframe as you type, using a smooth 400ms debounce to prevent constant server load.
- **Error Visualization**: Captures Template Syntax Errors, Undefined Variables, and JSON Syntax errors, rendering an inline dark warning frame indicating the error type and line number.
- **Pre-configured Templates (Presets)**:
  - **Invoice Template**: Demonstrates conditional state badges, variable formatting, currency formatting, and list iteration.
  - **Welcome Email**: Demonstrates HTML emails, conditionals, dates, and text formatting.
  - **User Profile Card**: Demonstrates avatar loading, skills list tags, theme configuration, and fallback filters.
  - **Conditionals & Loops**: Basic playground highlighting the standard Jinja control blocks.
- **Responsive Viewport Controls**: Instantly test how templates render across different screen resolutions:
  - 🖥️ **Desktop** (100% width)
  - 📱 **Tablet** (768px width)
  - 🔌 **Mobile** (375px width)
- **Export Capabilities**:
  - 📋 **Copy HTML**: Copies compiled template code to your clipboard.
  - 📥 **Download**: Downloads the rendered HTML directly as a file.
  - 🔗 **Open Full Screen**: Launches the rendered preview in a new window/tab.

---

## Custom Filters

The sandbox includes the following custom Jinja2 filters for formatting:

| Filter | Description | Usage Example | Result |
| :--- | :--- | :--- | :--- |
| `currency` | Formats a float or integer to currency structure. | `{{ 1249.50 \| currency }}` | `$1,249.50` |
| `date(format)`| Parsers a timestamp/date string. | `{{ "2026-06-05" \| date("%d %b %Y") }}` | `05 Jun 2026` |
| `mask(type)` | Obfuscates email/card credentials. | `{{ "alex@company.com" \| mask("email") }}` | `a**x@company.com` |
| `slugify` | Converts strings to URL-friendly slugs. | `{{ "Hello Jinja Sandbox!" \| slugify }}` | `hello-jinja-sandbox` |

---

## Quick Start using UV

This project is set up and managed using [uv](https://github.com/astral-sh/uv), a fast Python package installer and resolver.

### 1. Run the Application
You can directly start the FastAPI server with:
```bash
uv run python main.py
```

### 2. Access the Live Editor
Once the server is running, open your web browser and navigate to:
```
http://localhost:8000
```
Change any template values or variables in the left panels, and watch the preview update on the right instantly!
