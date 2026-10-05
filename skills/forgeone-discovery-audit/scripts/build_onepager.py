#!/usr/bin/env python3
"""Build the screen-shareable discovery one-pager from data.json.

Reads  <root>/data.json
Writes <root>/Discovery-<slug>.html  (self-contained, charte ForgeOne v5 "Editorial SaaS")

Angle = ANALYSE DE MARCHÉ SEO : la demande réelle du marché, ce qui rank (les contenus/
pages qui gagnent), où le prospect se situe, et ses ouvertures SEO. Le potentiel € reste
en note légère, jamais en hero. Conçu pour être partagé en écran pendant un call discovery.

DA ForgeOne v5 (réf ~/Desktop/forgeone-home.html) : near-white, hairlines 1px, UN bleu
#075CD8, Figtree + JetBrains Mono, jamais de gros aplat coloré, seul bloc sombre = CTA final.
"""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path

esc = html.escape


def fmt_int(n):
    try:
        return f"{int(round(float(n))):,}".replace(",", " ")
    except (ValueError, TypeError):
        return "—"


CSS = """
:root{
  --paper:#FFFFFF; --bone:#F6F7F9; --panel:#F3F4F6;
  --ink:#0B0B0F; --carbon:#1D1D20; --graphite:#636F7B; --pencil:#8C9BAA;
  --blue:#075CD8; --blue-deep:#0A50FF; --sky:#DCE9FF;
  --line:#E7E9EE; --green:#1c7a45;
  --p-yellow:#FFF3C4; --p-mint:#CFF3DE; --p-pink:#FFD9E4; --p-lav:#E6DCFF; --p-peach:#FFE4CC; --p-blue:#DCE9FF;
  --font:'Figtree',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; --mono:'JetBrains Mono',ui-monospace,monospace;
  --r-card:20px; --r-feat:32px; --r-pill:999px;
  --sh:rgba(11,11,20,.06) 0 0 18px 0; --sh-float:rgba(11,11,20,.08) 0 12px 34px -8px, rgba(11,11,20,.05) 0 2px 6px;
}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bone);color:var(--ink);font-family:var(--font);font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased}
.wrap{max-width:920px;margin:0 auto;padding:0 32px}
.mono{font-family:var(--mono);letter-spacing:.04em}

/* header */
.top{display:flex;align-items:center;justify-content:space-between;padding:26px 0 6px}
.logo{font-weight:800;font-size:20px;letter-spacing:-.04em;display:flex;align-items:center;gap:9px}
.logo i{width:15px;height:15px;background:var(--blue);border-radius:5px;transform:rotate(45deg)}
.top .meta{text-align:right;font-family:var(--mono);font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--pencil);line-height:1.5}

/* hero */
.hero{position:relative;padding:28px 0 14px;overflow:hidden}
.hero .wash{position:absolute;top:-140px;left:-60px;width:720px;height:420px;z-index:0;pointer-events:none;
  background:radial-gradient(circle at 40% 40%,rgba(7,92,216,.12),rgba(220,233,255,.30) 44%,transparent 70%)}
.hero>*{position:relative;z-index:1}
.hero .k{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--blue)}
.hero h1{font-size:clamp(32px,5vw,50px);line-height:1;letter-spacing:-.045em;font-weight:800;margin:10px 0 8px}
.hero .sub{font-size:16px;color:var(--graphite);max-width:62ch}

/* sections */
.section{padding:18px 0}
.section h2{font-size:22px;font-weight:800;letter-spacing:-.03em;margin-bottom:3px}
.section .hint{font-size:13px;color:var(--graphite);margin-bottom:14px;max-width:70ch}
.card{background:var(--paper);border:1px solid var(--line);border-radius:var(--r-card)}

/* demand bars */
.demand{padding:20px 24px}
.drow{display:grid;grid-template-columns:1fr 220px 62px;align-items:center;gap:14px;padding:7px 0;border-top:1px solid var(--line)}
.drow:first-child{border-top:0}
.drow .th{font-size:14px;font-weight:600;color:var(--carbon)}
.drow .track{height:10px;background:var(--panel);border-radius:999px;overflow:hidden}
.drow .track i{display:block;height:100%;background:var(--sky);border-radius:999px}
.drow .track i.hot{background:var(--blue)}
.drow .v{font-family:var(--mono);font-size:12.5px;text-align:right;color:var(--graphite)}

/* what works — insight + examples */
.works{padding:24px 26px;box-shadow:var(--sh-float)}
.works .tag{display:inline-flex;font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;padding:4px 10px;border-radius:var(--r-pill);background:var(--p-mint);color:var(--green);font-weight:600;margin-bottom:12px}
.works .lead{font-size:17px;font-weight:600;letter-spacing:-.01em;line-height:1.35;max-width:64ch}
.works .ex{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:18px}
.exi{background:var(--bone);border:1px solid var(--line);border-radius:14px;padding:14px 16px}
.exi h4{font-size:13.5px;font-weight:700}
.exi p{font-size:12.5px;color:var(--graphite);margin-top:4px;line-height:1.5}
.exi .u{font-family:var(--mono);font-size:11px;color:var(--blue);margin-top:6px;word-break:break-all}

/* benchmark bars */
.bench{padding:22px 26px}
.brow{display:grid;grid-template-columns:180px 1fr 82px;align-items:center;gap:14px;padding:6px 0}
.brow .nm{font-size:13.5px;font-weight:600;text-align:right;color:var(--carbon);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.brow .track{height:22px;background:var(--panel);border:1px solid var(--line);border-radius:8px;overflow:hidden}
.brow .track i{display:block;height:100%;background:var(--sky);border-radius:7px}
.brow.ceiling .track i{background:var(--blue)}
.brow.avg .track i{background:var(--green)} .brow.avg .nm{color:var(--green)}
.brow.client .track i{background:var(--pencil)} .brow.client .nm{color:var(--ink);font-weight:800}
.coverage{margin-top:14px;font-size:13px;color:var(--graphite)}
.coverage b{color:var(--ink)}

/* openings */
.opens{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.open{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:18px 20px}
.open .n{width:26px;height:26px;border-radius:8px;background:var(--sky);color:var(--blue);display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;margin-bottom:11px;font-family:var(--mono)}
.open h4{font-size:15px;font-weight:700;letter-spacing:-.01em}
.open p{font-size:13px;color:var(--graphite);margin-top:5px;line-height:1.5}

/* potential note */
.pot{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:18px 22px;margin-top:6px;font-size:14px;color:var(--graphite)}
.pot b{color:var(--ink)}


/* conversion projection */
.conv{padding:22px 26px}
.conv .src{display:inline-flex;font-family:var(--mono);font-size:10px;letter-spacing:.08em;text-transform:uppercase;padding:4px 10px;border-radius:var(--r-pill);background:var(--p-blue);color:var(--blue);font-weight:600;margin-bottom:12px}
.crow{display:grid;grid-template-columns:200px 1fr 190px;align-items:center;gap:14px;padding:10px 0;border-top:1px solid var(--line)}
.crow:first-of-type{border-top:0}
.crow .nm{font-size:14px;font-weight:600;color:var(--carbon)}
.crow .tr{font-family:var(--mono);font-size:12px;color:var(--pencil)}
.crow .big{font-size:20px;font-weight:800;letter-spacing:-.03em;text-align:right}
.crow .big small{display:block;font-size:12px;font-weight:500;color:var(--graphite);letter-spacing:0}
.crow.client .nm{font-weight:800;color:var(--ink)}
.crow.avg .big{color:var(--green)}
.conv .note{margin-top:12px;font-size:12.5px;color:var(--graphite);line-height:1.55}
.conv .todo{font-size:14px;color:var(--graphite);background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px}

/* final CTA on ink */
.final{background:var(--ink);color:#fff;border-radius:var(--r-feat);padding:38px 40px;margin:22px 0 8px;text-align:center}
.final .k{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#7FA6FF}
.final h3{font-size:clamp(21px,2.8vw,28px);font-weight:800;letter-spacing:-.03em;color:#fff;margin:10px auto 0;max-width:30ch;line-height:1.14}

.foot{padding:18px 0 34px;border-top:1px solid var(--line);font-size:11px;color:var(--pencil);line-height:1.6}
.foot b{color:var(--graphite);font-weight:600}
@media(max-width:760px){.works .ex,.opens{grid-template-columns:1fr}.drow{grid-template-columns:1fr 120px 58px}.brow{grid-template-columns:120px 1fr 70px}.crow{grid-template-columns:1fr;gap:4px}.crow .big{text-align:left}.wrap{padding:0 20px}}
@media print{body{background:#fff}.hero .wash{display:none}}
"""


def demand_html(demand):
    if not demand:
        return ""
    mx = max((float(d.get("volume") or 0) for d in demand), default=1) or 1
    rows = ""
    for d in demand:
        vol = float(d.get("volume") or 0)
        w = max(4, round(vol / mx * 100))
        hot = " hot" if vol >= mx * 0.6 else ""
        rows += (f'<div class="drow"><div class="th">{esc(str(d.get("theme") or ""))}</div>'
                 f'<div class="track"><i class="{hot.strip()}" style="width:{w}%"></i></div>'
                 f'<div class="v">{fmt_int(vol)}</div></div>')
    return (f'<div class="section"><h2>Le marché en un coup d\'œil</h2>'
            f'<div class="hint">Ce que votre marché tape vraiment chaque mois (recherches Google). C\'est là qu\'est la demande.</div>'
            f'<div class="card demand">{rows}</div></div>')


def works_html(w):
    if not w:
        return ""
    ex = ""
    for e in (w.get("examples") or []):
        ex += (f'<div class="exi"><h4>{esc(str(e.get("pattern") or ""))}</h4>'
               + (f'<p>{esc(str(e.get("detail")))}</p>' if e.get("detail") else '')
               + (f'<div class="u">{esc(str(e.get("proof")))}</div>' if e.get("proof") else '') + '</div>')
    return (f'<div class="section"><h2>Ce qui marche dans votre marché</h2>'
            f'<div class="hint">Le schéma que les gagnants de votre secteur exploitent, et que vous pouvez répliquer.</div>'
            f'<div class="card works"><span class="tag">Le signal</span>'
            f'<div class="lead">{esc(str(w.get("summary") or ""))}</div>'
            + (f'<div class="ex">{ex}</div>' if ex else '') + '</div></div>')


def bench_html(competitors, coverage):
    if not competitors:
        return ""
    mx = max((float(c.get("traffic") or 0) for c in competitors), default=1) or 1
    ordered = sorted(competitors, key=lambda c: float(c.get("traffic") or 0), reverse=True)
    bars = ""
    for c in ordered:
        role = c.get("role", "")
        cls = f"brow {role}" if role in ("client", "avg", "ceiling") else "brow"
        w = max(3, round(float(c.get("traffic") or 0) / mx * 100))
        bars += (f'<div class="{cls}"><div class="nm">{esc(str(c.get("name") or ""))}</div>'
                 f'<div class="track"><i style="width:{w}%"></i></div>'
                 f'<div class="v">{fmt_int(c.get("traffic"))}</div></div>')
    cov = f'<div class="coverage">{coverage}</div>' if coverage else ''
    return (f'<div class="section"><h2>Vous, face à votre marché</h2>'
            f'<div class="hint">Trafic organique mensuel estimé. En vert la moyenne du marché, en bleu le meilleur.</div>'
            f'<div class="card bench">{bars}{cov}</div></div>')


def fmt_pct(r):
    return f"{float(r) * 100:.1f}".replace(".", ",").rstrip("0").rstrip(",") + " %"


def conversion_html(cp, competitors):
    """Projection de ventes / demandes de devis. Le taux est celui du prospect si connu,
    sinon une fourchette sourcée. Même taux pour tous : on compare le trafic, pas la
    conversion (le taux d'un concurrent n'est pas observable). Sans taux : emplacement à remplir."""
    if not cp:
        return ""
    unit = str(cp.get("unit") or "ventes")
    mid = cp.get("rate_mid")
    if mid in (None, ""):
        body = ('<div class="todo">Taux de conversion à renseigner pendant l\'appel : '
                'c\'est votre chiffre réel qui rend la projection la vôtre.</div>')
        return (f'<div class="section"><h2>Ce que ce trafic représenterait</h2>'
                f'<div class="card conv">{body}</div></div>')
    mid = float(mid)
    low = float(cp.get("rate_low") or mid)
    high = float(cp.get("rate_high") or mid)
    val = cp.get("value_per_conversion")
    rows = ""
    for c in sorted(competitors or [], key=lambda c: float(c.get("traffic") or 0)):
        role = c.get("role", "")
        if role not in ("client", "avg", "ceiling"):
            continue
        t = float(c.get("traffic") or 0)
        lo, hi = round(t * low), round(t * high)
        rng = f"{fmt_int(lo)} à {fmt_int(hi)}" if lo != hi else fmt_int(lo)
        eur = ""
        if val not in (None, ""):
            eur = f"<small>soit {fmt_int(t * mid * float(val))} € par mois</small>"
        else:
            eur = f"<small>{unit} par mois</small>"
        rows += (f'<div class="crow {role}"><div class="nm">{esc(str(c.get("name") or ""))}</div>'
                 f'<div class="tr">{fmt_int(t)} visiteurs par mois</div>'
                 f'<div class="big">{rng} {unit}{eur}</div></div>')
    if not rows:
        return ""
    if cp.get("rate_source") == "prospect":
        tag = f"Votre taux réel : {fmt_pct(mid)}"
        note = "Calcul sur le taux de conversion que vous nous avez communiqué."
    else:
        tag = f"Fourchette de marché : {fmt_pct(low)} à {fmt_pct(high)}"
        note = ("Faute de votre chiffre réel, fourchette de marché. "
                + esc(str(cp.get("sources") or "Source à préciser.")))
    note += (" Le même taux est appliqué à tout le monde : on compare le trafic, "
             "pas la conversion, car celle d'un concurrent n'est pas visible de l'extérieur.")
    return (f'<div class="section"><h2>Ce que ce trafic représenterait</h2>'
            f'<div class="hint">Une projection pour vous situer : combien de {unit} par mois selon le trafic capté.</div>'
            f'<div class="card conv"><span class="src">{esc(tag)}</span>{rows}'
            f'<div class="note">{note}</div></div></div>')


def opens_html(openings):
    if not openings:
        return ""
    cards = ""
    for i, o in enumerate(openings, start=1):
        cards += (f'<div class="open"><div class="n">{i:02d}</div>'
                  f'<h4>{esc(str(o.get("title") or ""))}</h4>'
                  + (f'<p>{esc(str(o.get("detail")))}</p>' if o.get("detail") else '') + '</div>')
    return (f'<div class="section"><h2>Vos ouvertures SEO</h2>'
            f'<div class="hint">Là où vous pouvez gagner vite, sur la base de ce que le marché récompense déjà.</div>'
            f'<div class="opens">{cards}</div></div>')


def build(data):
    prospect = esc(str(data.get("prospect") or "Prospect"))
    potential = data.get("potential")
    next_step = data.get("next_step") or ""
    foot = data.get("footnote") or ""

    pot_html = f'<div class="section"><div class="pot">{esc(str(potential))}</div></div>' if potential else ''
    final_html = (f'<div class="final"><div class="k">La prochaine étape</div><h3>{esc(str(next_step))}</h3></div>') if next_step else ''

    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Analyse de marché SEO — {prospect}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<div class="wrap">
  <div class="top">
    <div class="logo"><i></i>Forgeone</div>
    <div class="meta">Analyse de marché SEO<br>{esc(str(data.get("date") or ""))}</div>
  </div>
  <div class="hero">
    <div class="wash"></div>
    <div class="k">Préparé pour votre appel</div>
    <h1>{prospect}</h1>
    <div class="sub">{esc(str(data.get("market") or ""))}</div>
  </div>
  {demand_html(data.get("market_demand"))}
  {works_html(data.get("what_works"))}
  {bench_html(data.get("competitors"), data.get("coverage"))}
  {conversion_html(data.get("conversion_projection"), data.get("competitors"))}
  {opens_html(data.get("openings"))}
  {pot_html}
  {final_html}
  <div class="foot">
    {f'<b>Méthode :</b> {esc(str(foot))}<br>' if foot else ''}
    Volumes et trafic organiques estimés (données DataForSEO, {esc(str(data.get("date") or ""))}). Analyse de cadrage, approfondie lors de l'Audit Croissance 360.
  </div>
</div>
</body></html>"""


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: build_onepager.py <workspace-root>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1]).expanduser()
    dj = root / "data.json"
    if not dj.exists():
        print(f"missing {dj}", file=sys.stderr)
        return 1
    data = json.loads(dj.read_text(encoding="utf-8"))
    slug = (data.get("prospect") or "prospect").lower().replace(" ", "-")
    out = root / f"Discovery-{slug}.html"
    out.write_text(build(data), encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
