
import re, json
from pathlib import Path
import flask
from cfcserver.models.appconfig import AppConfig


def render_svelte(page_body, view_model=None):
    args = {}
    page_json = json.dumps(
        view_model or {},
        default=lambda o: o.__dict__,   # for serializing SimpleNamespaces
        separators=(',', ':') if AppConfig.IS_PROD else None,
        indent=None if AppConfig.IS_PROD else 2,
    )
    # ---- Escape chars that are "dangerous" inside the <script> tag.
    replacements = {
        # '\\': r'\u005c',  # No! since json.dumps escapes with \" inside "strings"
        '&': r'\u0026',     # Prevent interpreting as &vars;
        '<': r'\u003c'      # Prevent interpreting as <tags>, </script>
    }
    for old, new in replacements.items():
        if old in page_json:    # .replace only if necessary (can be huge strings)
            page_json = page_json.replace(old, new)
    args['page_json'] = page_json

    if '<' not in page_body:
        # No '<' means no HTML tags; means it's just a component name
        args['page_component'] = page_body
    else:
        # '<' means has HTML tags; means it goes inside the <body>
        args['page_body'] = page_body
    return flask.render_template('svelte.html', **args)


def get_built_url_format():
    project_dir = Path(__file__).resolve().parents[3]
    built_confg_fp = project_dir / 'x-dev/rollupjs/built.config.js'
    with open(built_confg_fp, 'rt') as bc:
        built_config = str(bc.read())
    pattern = r'dest_dir\s*[:=]\s*["\']([^"\']*)["\']'
    s = re.search(pattern, built_config)
    built_dir = s.group(1) if s else 'NOT_SET'
    return f'/static/{built_dir}/{{}}'
