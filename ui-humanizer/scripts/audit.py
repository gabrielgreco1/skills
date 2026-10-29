#!/usr/bin/env python3
"""Grep heuristico dos tells de UI gerada por IA (ver SKILL.md).

Uso: python3 -I audit.py <arquivo-ou-pasta> [...]
Saida: arquivo:linha  [ID] descricao  | trecho
"""
import re
import sys
from pathlib import Path

EXTS = {".html", ".htm", ".css", ".scss", ".jsx", ".tsx", ".js", ".ts", ".vue", ".svelte", ".astro", ".md", ".mdx"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", "out", "coverage", ".venv", "vendor"}

EMOJI = "[\U0001F300-\U0001FAFF☀-➿⭐✨]"

RULES = [
    ("A1", "eyebrow: texto pequeno caixa alta com tracking largo",
     r"(uppercase[^\"'`]*tracking-(wide|wider|widest|\[)|tracking-(wider|widest|\[[^\]]+\])[^\"'`]*uppercase|text-transform:\s*uppercase[^}]*letter-spacing|letter-spacing:\s*0?\.\d+em[^}]*text-transform:\s*uppercase|class=[\"'][^\"']*\b(eyebrow|kicker|overline|section-label)\b)"),
    ("A2", "texto em gradiente",
     r"(bg-clip-text|background-clip:\s*text|-webkit-background-clip:\s*text|-webkit-text-fill-color:\s*transparent)"),
    ("A3", "headline bicolor (span colorido dentro do h1/h2)",
     r"<h[12][^>]*>[^<]*(<[^>]+>[^<]*)*<span[^>]*class=[\"'][^\"']*\btext-(primary|accent|brand|blue|indigo|violet|purple|amber|yellow|orange|emerald|green|sky|cyan|pink|rose)"),
    ("A4", "display serif da moda (checar se o titulo termina em italico)",
     r"(Playfair|Instrument\s*Serif|DM\s*Serif|Fraunces|Cormorant|Newsreader)"),
    ("A5", "borda lateral/superior pintada",
     r"(border-left:\s*[2-8]px\s+solid|border-l-([2-8]|\[[2-8]px\])\b|border-t-[4-8]\b|border-inline-start:\s*[2-8]px|inset\s+[3-6]px\s+0\s+0)"),
    ("A7", "bolinha/elemento pulsando",
     r"(animate-ping|animate-pulse|@keyframes\s+(pulse|ping|blink)\b)"),
    ("A8", "sparkle / 'powered by AI' no topo",
     r"(\bSparkles\b|lucide-sparkles|(?i:powered by ai|feito com ia|ai-powered))"),
    ("A9", "emoji como icone/bullet", EMOJI),
    ("A10", "roxo/indigo padrao do Tailwind",
     r"(\b(violet|indigo|purple|fuchsia)-(400|500|600|700)\b|#(8b5cf6|7c3aed|6366f1|4f46e5|a855f7|9333ea|6d28d9)\b)"),
    ("A11", "numero dentro de circulo (passos 1-2-3)",
     r"rounded-full[^\"'`]*\b(w|h|size)-(6|7|8|9|10|11|12)\b[^>]*>\s*(0?[1-9])\s*<"),
    ("A12", "glassmorphism",
     r"(backdrop-filter:\s*blur|backdrop-blur|bg-white/(5|10|15|20)\b)"),
    ("A13", "hover levantando/escala (checar se o elemento e clicavel)",
     r"(hover:-?translate-y|hover:scale-|hover:shadow-(xl|2xl)|:hover[^{]*\{[^}]*transform:\s*(translateY|scale))"),
    ("B3", "icone em quadradinho colorido",
     r"(rounded-(lg|xl|2xl)[^\"'`]*bg-[a-z]+-(50|100)\b[^\"'`]*p-[2-3]|bg-(primary|accent)/(5|10|15)\b[^\"'`]*rounded)"),
    ("B5", "pill/raio grande",
     r"(rounded-full|rounded-(2xl|3xl)|border-radius:\s*(9999px|999px|50px|100px))"),
    ("B6", "gradiente de fundo / glow",
     r"(bg-gradient-to-|linear-gradient\(|radial-gradient\(|conic-gradient\(|blur-3xl)"),
    ("B7", "animacao de scroll/entrada generica",
     r"(fade-?up|fadeInUp|data-aos|animate-fade|whileInView|animate-marquee)"),
    ("B11", "copy de template",
     r"(?i)(comece agora|get started( for free| today)?|sem complica|solu[cç][aã]o completa|tudo em um s[oó] lugar|por que escolher|chega de |sem cart[aã]o de cr[eé]dito|seamless(ly)?|supercharge|unlock (the|your)|elevate your|all-in-one|everything you need|transform[ea]? (your|seu|sua)|revolucion|potencializ|next[- ]level|trusted by|join thousands|\+\s?\d{1,3}[.,]?\d{3}\+? (clientes|usu[aá]rios|users|customers))"),
    ("C4", "CTA em caixa alta com seta",
     r"(?i)>\s*(SAIBA MAIS|CONSULTE AQUI|ACESSE AQUI|VER MAIS|LEARN MORE)\s*(→|&rarr;|<)"),
    ("E2", "scroll cue ('role pra baixo' / chevron pulando)",
     r"(?i)(scroll (down|to explore)|role (pra|para) (baixo|explorar)|animate-bounce)"),
    ("E4", "pilula de versao/estado no hero (BETA, V0.x, EARLY ACCESS)",
     r"(?i)>\s*(beta|early access|invite[- ]only|v0?\.\d|coming soon)\s*<"),
    ("E6", "fundo de grade/bolinha decorativo",
     r"(repeating-linear-gradient|mask-image:[^;]*radial-gradient|bg-\[radial-gradient|bg-grid|\[background-size:[^\]]*px_[^\]]*px\])"),
    ("E9", "easing de mola/salto",
     r"(easeOutBack|easeInBack|\belastic\b|backOut|cubic-bezier\([^)]*,\s*-[0-9.])"),
    ("E13", "texto cinza sobre superficie colorida",
     r"(?i)bg-(indigo|violet|purple|blue|emerald|rose|teal|sky|cyan)-(500|600|700|800)[^\"'`]*text-(gray|zinc|slate|neutral|stone)-(300|400|500)"),
    ("E14", "corpo justificado ou caixa alta",
     r"(text-align:\s*justify|text-justify|\btext-justify\b)"),
]
COMPILED = [(i, d, re.compile(p)) for i, d, p in RULES]


def files(paths):
    for p in map(Path, paths):
        if p.is_file():
            yield p
        elif p.is_dir():
            for f in p.rglob("*"):
                if f.is_file() and f.suffix.lower() in EXTS and not (SKIP_DIRS & set(f.parts)):
                    yield f


def main(argv):
    if not argv:
        print(__doc__.strip())
        return 2
    counts = {}
    for f in files(argv):
        try:
            lines = f.read_text(errors="ignore").splitlines()
        except OSError:
            continue
        for n, line in enumerate(lines, 1):
            if len(line) > 2000:
                line = line[:2000]
            for rid, desc, rx in COMPILED:
                m = rx.search(line)
                if m:
                    counts[rid] = counts.get(rid, 0) + 1
                    s = max(0, m.start() - 40)
                    snippet = line[s:m.end() + 40].strip()
                    print(f"{f}:{n}  [{rid}] {desc}  | {snippet}")
    print("\nResumo:")
    for rid, desc, _ in COMPILED:
        if rid in counts:
            print(f"  {rid:4} {counts[rid]:4}x  {desc}")
    if not counts:
        print("  nenhum tell com assinatura no codigo (ainda vale olhar a pagina renderizada)")
    print("\nA* = aja na 1a ocorrencia; B* = pesa em conjunto; C* = so com companhia. Detalhes em references/tells.md. Tells so visuais (layout padrao,"
          " cards iguais, falta de imagem, cara de SaaS) nao aparecem aqui.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
