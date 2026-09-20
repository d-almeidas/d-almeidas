"""Adiciona uma barra de progresso animada embaixo da cobrinha do snk.

A barra enche na mesma duração da animação da cobrinha e reinicia junto com ela,
então os dois ficam em loop, sincronizados.

Uso: python3 add_progress_bar.py caminho/do/github-snake.svg
"""
import re
import sys

TRACK = "#21262d"  # fundo da barra
FILL = "#8b949e"   # parte preenchida

path = sys.argv[1]
svg = open(path, encoding="utf-8").read()

# duração total da animação (o snk escreve algo como "83700ms linear infinite")
m = re.search(r"(\d+)ms linear infinite", svg)
duration = int(m.group(1)) if m else 20000

# área do desenho: viewBox="x y largura altura"
vb = re.search(r'viewBox="(-?[\d.]+) (-?[\d.]+) ([\d.]+) ([\d.]+)"', svg)
if not vb:
    sys.exit("viewBox não encontrado, barra não adicionada")
x0, y0, w, h = (float(v) for v in vb.groups())

bar_x = 0
bar_w = w + 2 * x0      # largura da grade de contribuições (sem as margens)
bar_h = 6
extra = 24              # espaço novo embaixo, para a barra não ficar no caminho da cobrinha
bar_y = y0 + h + 8

# aumenta a altura da imagem para caber a barra
svg = svg.replace(vb.group(0), f'viewBox="{x0:g} {y0:g} {w:g} {h + extra:g}"', 1)
root = re.match(r"<svg[^>]*>", svg).group(0)
novo_root = re.sub(
    r'height="([\d.]+)"', lambda mm: f'height="{float(mm.group(1)) + extra:g}"', root, count=1
)
svg = svg.replace(root, novo_root, 1)

keyframes = "@keyframes pb{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
svg = svg.replace("</style>", keyframes + "</style>", 1)

barra = (
    f'<g>'
    f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="3" fill="{TRACK}"/>'
    f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="3" fill="{FILL}" '
    f'style="transform-box:fill-box;transform-origin:left center;'
    f'animation:pb {duration}ms linear infinite"/>'
    f'</g>'
)
svg = svg.replace("</svg>", barra + "</svg>")

open(path, "w", encoding="utf-8").write(svg)
print(f"barra adicionada: {duration} ms de duração")
