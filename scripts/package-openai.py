#!/usr/bin/env python3
"""Validate the plugin against OpenAI's directory rules and build the upload zip.

Usage: python3 scripts/package-openai.py   ->   dist/ramus-openai-plugin.zip

The zip holds only what the OpenAI plugin portal reads: plugin.json, mcp.json,
skills/ and the listing assets. Files for other clients stay out of it
(.mcp.json and .claude-plugin/ use Claude Code's userConfig, which OpenAI does
not support; gemini-extension.json and server.json are for other registries).
Limits follow https://developers.openai.com/plugins/deploy/submission-errors.
"""
import json, re, struct, sys, unicodedata, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'dist' / 'ramus-openai-plugin.zip'
CATEGORIES = {'Productivity', 'Creativity', 'Developer Tools', 'Business & Operations', 'Data & Analytics',
              'Communication', 'Education & Research', 'Security', 'Finance', 'Healthcare', 'Travel',
              'Entertainment', 'Other'}
errors = []
def check(ok, message):
    if not ok: errors.append(message)

def luminance(hex_color):
    channels = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]

def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)

def png_size(path):
    with open(path, 'rb') as f:
        head = f.read(24)
    if head[:8] != b'\x89PNG\r\n\x1a\n': return None
    return struct.unpack('>II', head[16:24])

plugin = json.loads((ROOT / 'plugin.json').read_text())
check(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}', plugin.get('name', '')) is not None, 'plugin name')
check(re.fullmatch(r'\d+\.\d+\.\d+([-+].*)?', plugin.get('version', '')) is not None, 'version must be semver')
check(1 <= len(plugin.get('description', '')) <= 1024, 'description 1-1024 chars')
check(1 <= len(plugin.get('author', {}).get('name', '')) <= 120, 'author.name 1-120 chars')

ui = plugin.get('extensions', {}).get('com.openai', {}).get('interface', {})
for field, limit in (('displayName', 30), ('shortDescription', 30), ('developerName', 80)):
    value = ui.get(field, '')
    check(0 < len(value) <= limit and '\n' not in value, f'{field}: 1-{limit} chars, one line (is {len(value)})')
check(0 < len(ui.get('longDescription', '')) <= 4000, 'longDescription: 1-4000 chars')
check(ui.get('category') in CATEGORIES, f'category must be one of {sorted(CATEGORIES)}')
prompts = ui.get('defaultPrompt', [])
prompts = [prompts] if isinstance(prompts, str) else prompts
check(len(prompts) <= 3, 'at most 3 defaultPrompt entries')
check(all(len(p) <= 128 and '@' not in p for p in prompts), 'defaultPrompt: each <= 128 chars, no @mentions')
check(len({unicodedata.normalize('NFKC', p) for p in prompts}) == len(prompts), 'defaultPrompt entries must be unique')
for field in ('websiteURL', 'privacyPolicyURL', 'termsOfServiceURL', 'supportURL'):
    url = ui.get(field)
    check(url is None or (url.startswith('https://') and len(url) <= 1024 and '@' not in url), f'{field}: https, <= 1024 chars')
for field, background in (('brandColor', '#ffffff'), ('brandColorDark', '#212121')):
    color = ui.get(field)
    if color is not None:
        check(re.fullmatch(r'#[0-9a-fA-F]{6}', color) is not None and contrast(color, background) >= 2,
              f'{field}: six-digit hex with >= 2:1 contrast against {background}')
for field in ('logo', 'composerIcon'):
    path = ROOT / ui.get(field, '')
    size = png_size(path) if path.is_file() else None
    check(size is not None and size[0] == size[1] and 48 <= size[0] <= 4096 and path.stat().st_size <= 5 << 20,
          f'{field}: square PNG, 48-4096 px, <= 5 MiB')

mcp = json.loads((ROOT / 'mcp.json').read_text())
for name, server in mcp.get('mcpServers', {}).items():
    check(server.get('url', '').startswith('https://') and 'headers' not in server, f'mcp server {name}: https URL, no static headers')

skills = sorted(p.parent for p in (ROOT / 'skills').glob('*/SKILL.md'))
check(skills, 'at least one skill')
names = set()
for skill in skills:
    text = (skill / 'SKILL.md').read_text()
    front = re.match(r'---\n(.*?)\n---\n(.*)', text, re.S)
    check(front is not None, f'{skill.name}: SKILL.md needs YAML front matter')
    if not front: continue
    meta = dict(re.findall(r'^(\w[\w-]*):\s*(.*)$', front.group(1), re.M))
    check(meta.get('name') and meta['name'] not in names, f'{skill.name}: unique name')
    names.add(meta.get('name'))
    check(0 < len(meta.get('description', '')) <= 1024, f'{skill.name}: description 1-1024 chars')
    check(front.group(2).strip() != '', f'{skill.name}: instructions must not be empty')
    check(len(plugin['name']) + len(meta.get('name', '')) <= 64, f'{skill.name}: plugin + skill name <= 64 chars')
    check(not re.search(r'\bclaude\b', text, re.I), f'{skill.name}: use provider-neutral wording (mentions Claude)')

if errors:
    print('Package is not ready:\n- ' + '\n- '.join(errors))
    sys.exit(1)

files = [ROOT / 'plugin.json', ROOT / 'mcp.json', ROOT / 'LICENSE', ROOT / ui['logo']]
files += [p for skill in skills for p in sorted(skill.rglob('*')) if p.is_file()]
OUT.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as archive:
    for path in dict.fromkeys(files):
        archive.write(path, path.relative_to(ROOT).as_posix())
print(f'OK: {OUT.relative_to(ROOT)}')
for name in zipfile.ZipFile(OUT).namelist():
    print('  ' + name)
