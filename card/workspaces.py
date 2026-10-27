"""Small linked cards for the README's workspaces row, one SVG per workspace and palette.

Run with: python -m card.workspaces
Writes workspaces/<org>_<mode>.svg. The org avatar is embedded, since GitHub blocks images an SVG loads itself.
"""
import base64
import html
import sys
import urllib.request

import yaml

from . import config

W, H, AVATAR, PAD = 480, 112, 72, 20


def card_svg(title, excerpt, avatar_png, theme):
    tx = PAD + AVATAR + 18
    img = base64.b64encode(avatar_png).decode()
    return f'''<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,'SFMono-Regular',Menlo,monospace" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><clipPath id="a"><rect x="{PAD}" y="{(H - AVATAR) / 2}" width="{AVATAR}" height="{AVATAR}" rx="12"/></clipPath></defs>
<rect width="{W}" height="{H}" rx="15" fill="{theme["bg"]}"/>
<image href="data:image/png;base64,{img}" x="{PAD}" y="{(H - AVATAR) / 2}" width="{AVATAR}" height="{AVATAR}" clip-path="url(#a)"/>
<text x="{tx}" y="{H / 2 - 6}" font-size="19px" font-weight="bold" fill="{theme["key"]}">{html.escape(title)}</text>
<text x="{tx}" y="{H / 2 + 20}" font-size="13px" fill="{theme["value"]}">{html.escape(excerpt)}</text>
</svg>
'''


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else config.ROOT / "config.yml"
    cfg = config.load(path)
    with open(path, encoding="utf-8") as f:
        workspaces = (yaml.safe_load(f) or {}).get("workspaces") or []
    out = cfg["root"] / "workspaces"
    out.mkdir(exist_ok=True)
    for ws in workspaces:
        with urllib.request.urlopen(f"https://github.com/{ws['org']}.png?size=144") as r:
            avatar = r.read()
        for mode, theme in cfg["themes"].items():
            path = out / f"{ws['org']}_{mode}.svg"
            path.write_text(card_svg(ws["title"], ws["excerpt"], avatar, theme), encoding="utf-8")
            print(f"wrote {path.relative_to(cfg['root'])}")


if __name__ == "__main__":
    main()
