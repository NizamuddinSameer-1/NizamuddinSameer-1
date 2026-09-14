#!/usr/bin/env python3
"""Draw the profile README's static graphics: the bookends of the session.

  hero.svg  SameerOS boot banner that greets the visitor
  exit.svg  the logout that closes the session

These never change, so the scheduled action doesn't touch them; run this by
hand after editing. Everything else on the page is drawn by
generate_stats.py from live GitHub data.
"""
import os

from generate_stats import WIDTH, head, fade, label

# Same chrome and accent tokens as status.svg, so all the windows on the page
# read as windows of one machine.
EXTRA = (".t-bg{fill:#f6f8fa}.t-b{stroke:#d0d7de}.p-u{fill:#0969da}.p-h{fill:#1a7f37}"
         "@media(prefers-color-scheme:dark){.t-bg{fill:#161b22}.t-b{stroke:#30363d}"
         ".p-u{fill:#58a6ff}.p-h{fill:#3fb950}}")

DOTS = ('<circle cx="18" cy="15" r="4.5" fill="#ff5f56"/>'
        '<circle cx="32" cy="15" r="4.5" fill="#ffbd2e"/>'
        '<circle cx="46" cy="15" r="4.5" fill="#27c93f"/>')


def chrome(h, title):
    """Window frame: traffic lights, centred title, hairline under the bar."""
    return (f'<g opacity="0">{fade(0.06)}'
            f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{h - 1}" rx="8" '
            f'class="t-bg t-b" stroke-width="1"/>' + DOTS
            + label(WIDTH / 2, 19, title, 11, "m-f", "middle",
                    ' letter-spacing="0.5"')
            + f'<line x1="0" y1="30" x2="{WIDTH}" y2="30" class="t-b" '
              f'stroke-width="1"/></g>')


def draw_hero():
    """The boot sequence: what the machine loads, then a welcome for the guest."""
    H = 210
    p = [head(WIDTH, H, extra=EXTRA)]
    p.append(chrome(H, "sameer@verse: /boot (tty1)"))

    rows = ['<text x="18" y="52" font-size="11" class="m-f">'
            'SameerOS v2.4 (x86_64 Linux) &#183; tty1</text>']
    services = ["mounted /autonomous-ai-workflows",
                "mounted /custom-media-bots",
                "started cloud-gpu-upscaling.service",
                "started multi-account-publisher.service",
                "reached target open-source-tools.target"]
    for i, svc in enumerate(services):
        y = 72 + i * 20
        rows.append(f'<text x="18" y="{y}" font-size="11" xml:space="preserve">'
                    f'<tspan class="p-h" font-weight="600">[  OK  ]</tspan> '
                    f'<tspan class="e-f">{svc}</tspan></text>')
    rows.append('<text x="18" y="176" font-size="11.5" class="e-f" '
                'font-weight="600">welcome, guest &#8211; this machine builds '
                '&amp; ships while i sleep.</text>')
    rows.append('<text x="18" y="198" font-size="11.5">'
                '<tspan class="p-u" font-weight="600">guest@verse</tspan>'
                '<tspan class="m-f">:</tspan>'
                '<tspan class="p-h" font-weight="600">~</tspan>'
                '<tspan class="m-f">$</tspan> '
                '<tspan class="e-f">scroll</tspan></text>')

    for i, markup in enumerate(rows):
        p.append(f'<g opacity="0">{fade(0.14 + i * 0.09, 0.30)}{markup}</g>')

    # The cursor outlives the boot: it keeps blinking, waiting for the scroll.
    p.append(f'<g opacity="0">{fade(0.92)}'
             f'<rect x="166" y="187" width="7" height="13" class="e-f">'
             f'<animate attributeName="opacity" values="1;0;1" dur="1.1s" '
             f'repeatCount="indefinite"/></rect></g>')
    p.append("</svg>")
    return "".join(p)


def draw_exit():
    """logout — the session closes the way it opened, in the terminal."""
    H = 104
    p = [head(WIDTH, H, extra=EXTRA)]
    p.append(chrome(H, "sameer@verse: ~ (zsh)"))
    rows = ['<text x="18" y="49" font-size="11.5">'
            '<tspan class="p-u" font-weight="600">guest@verse</tspan>'
            '<tspan class="m-f">:</tspan>'
            '<tspan class="p-h" font-weight="600">~</tspan>'
            '<tspan class="m-f">$</tspan> '
            '<tspan class="e-f" font-weight="600">exit</tspan></text>',
            '<text x="18" y="71" font-size="11" class="m-f">logout</text>',
            '<text x="18" y="91" font-size="11" class="m-f">'
            'Connection to sameerOS closed &#8211; thanks for visiting, '
            'guest.</text>']
    for i, markup in enumerate(rows):
        p.append(f'<g opacity="0">{fade(0.12 + i * 0.12, 0.30)}{markup}</g>')
    p.append("</svg>")
    return "".join(p)


def main():
    out = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       os.pardir))
    for name, svg in (("hero.svg", draw_hero()), ("exit.svg", draw_exit())):
        with open(os.path.join(out, name), "w", encoding="utf-8") as f:
            f.write(svg)
        print("wrote", name)


if __name__ == "__main__":
    main()
