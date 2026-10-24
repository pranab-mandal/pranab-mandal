"""Builds dark_mode.svg and light_mode.svg (neofetch-style GitHub profile card).
Edit the INFO section below, then run:  python build_svg.py
"""
from html import escape

USER = "pranab-mandal"
W = 58            # width (in characters) of the info column
STATS_DEFAULT = {"repos": "—", "contrib": "—", "stars": "—", "commits": "—", "followers": "—"}

# ----------------------------------------------------------------------------
#  EDIT YOUR INFO HERE  (text taken from your resume; phone number left out on purpose)
# ----------------------------------------------------------------------------
def info(stats):
    s = {**STATS_DEFAULT, **(stats or {})}
    return [
        ("title", "pranab@nith"),
        ("row", "OS", "Linux"),
        ("row", "Uptime", "B.Tech, 2nd Year (2025 - 2029)"),
        ("row", "Host", "NIT Hamirpur"),
        ("row", "Role", "Frontend Dev, E-Cell NIT Hamirpur"),
        ("row", "IDE", "VS Code"),
        ("blank",),
        ("row", "Languages.Programming", "JavaScript, Python, C, C++"),
        ("row", "Languages.Web", "HTML5, CSS3, React.js, Tailwind"),
        ("row", "Backend.Stack", "Node.js, Express.js, MongoDB"),
        ("row", "Tools", "Git, Linux, Android VpnService"),
        ("row", "Interests", "Web Dev, AI Agents, Network Security"),
        ("blank",),
        ("section", "Highlights"),
        ("row", "Hackathon", "1st Place, DRDO Sponsored Hackathon"),
        ("row", "Hackathon", "1st Place, HackSecure 26"),
        ("row", "Research", "Intern, CAIR - IIT Mandi (2026)"),
        ("row", "Project", "Packet Pulse, TenderScout"),
        ("blank",),
        ("section", "Contact"),
        ("row", "Email", "pranab947591@gmail.com"),
        ("row", "LinkedIn", "pranabmandal"),
        ("row", "GitHub", USER),
        ("blank",),
        ("section", "GitHub Stats"),
        ("pair", "Repos", s["repos"], "Contributed", s["contrib"]),
        ("pair", "Stars", s["stars"], "Commits", s["commits"]),
        ("row", "Followers", s["followers"]),
    ]

THEMES = {
    "dark_mode":  dict(bg="#161b22", fg="#c9d1d9", key="#ffa657", val="#a5d6ff", dots="#616e7f", art="#c9d1d9", border="#30363d"),
    "light_mode": dict(bg="#f6f8fa", fg="#24292f", key="#953800", val="#0a3069", dots="#b1bac4", art="#24292f", border="#d0d7de"),
}

ART_FONT, ART_LH, ART_X, ART_Y = 9, 10.6, 18, 28      # ASCII art size / line height / origin
TXT_FONT, TXT_LH, TXT_X, TXT_Y = 14, 20, 470, 34       # info text
CHAR_W = TXT_FONT * 0.602


def t(c, cls, text):
    return f'<tspan class="{cls}">{escape(text)}</tspan>'


def build_lines(stats):
    out = []
    for item in info(stats):
        kind = item[0]
        if kind == "blank":
            out.append("")
        elif kind == "title":
            out.append(t(0, "key", item[1]) + " " + t(0, "dots", "-" * (W - len(item[1]) - 1)))
        elif kind == "section":
            out.append(t(0, "fg", "- ") + t(0, "key", item[1]) + " " + t(0, "dots", "-" * (W - len(item[1]) - 3)))
        elif kind == "row":
            k, v = item[1], str(item[2])
            n = max(W - len(k) - len(v) - 2, 2)
            out.append(t(0, "key", k) + t(0, "dots", " " + "." * n + " ") + t(0, "val", v))
        elif kind == "pair":
            _, k1, v1, k2, v2 = item
            left = f"{k1}: {v1}"
            right = f"{k2}: {v2}"
            n = max(W - len(left) - len(right) - 4, 2)
            out.append(t(0, "key", k1 + ":") + t(0, "val", " " + str(v1)) + t(0, "dots", " " + "." * n + " ") +
                       t(0, "key", k2 + ":") + t(0, "val", " " + str(v2)))
    return out


def build(stats=None, ascii_path="ascii.txt"):
    art = open(ascii_path).read().split("\n")
    lines = build_lines(stats)
    width = int(TXT_X + W * CHAR_W + 24)
    height = int(max(ART_Y + len(art) * ART_LH, TXT_Y + len(lines) * TXT_LH) + 20)
    for name, c in THEMES.items():
        o = [f'<?xml version="1.0" encoding="UTF-8"?>',
             f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="ConsolasFallback,Consolas,\'DejaVu Sans Mono\',\'Courier New\',monospace">',
             '<style>@font-face{font-family:ConsolasFallback;font-display:swap;src:local(Consolas),local("DejaVu Sans Mono");size-adjust:109%}',
             f'.key{{fill:{c["key"]};font-weight:bold}}.val{{fill:{c["val"]}}}.dots{{fill:{c["dots"]}}}.fg{{fill:{c["fg"]}}}'
             f'.art{{fill:{c["art"]};font-size:{ART_FONT}px}}.txt{{font-size:{TXT_FONT}px;fill:{c["fg"]}}}</style>',
             f'<rect width="{width}" height="{height}" rx="15" fill="{c["bg"]}" stroke="{c["border"]}"/>',
             f'<text class="art" xml:space="preserve">']
        for i, ln in enumerate(art):
            o.append(f'<tspan x="{ART_X}" y="{ART_Y + i * ART_LH:.1f}">{escape(ln)}</tspan>')
        o.append("</text>")
        o.append('<text class="txt" xml:space="preserve">')
        for i, ln in enumerate(lines):
            if ln:
                o.append(f'<tspan x="{TXT_X}" y="{TXT_Y + i * TXT_LH}">{ln}</tspan>')
        o.append("</text></svg>")
        open(f"{name}.svg", "w", encoding="utf-8").write("\n".join(o))
    print("wrote dark_mode.svg and light_mode.svg")


if __name__ == "__main__":
    build()
