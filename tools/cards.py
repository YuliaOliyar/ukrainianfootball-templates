#!/usr/bin/env python3
"""Шаблони карток 1200×675 для статей агента + типові картинки рубрик. Пише в ../uf-templates/cards/."""
import os, html
OUT = os.path.join(os.path.dirname(__file__), "..", "uf-templates", "cards")
os.makedirs(os.path.join(OUT, "rubrics"), exist_ok=True)
E = html.escape
MARK = open(os.path.join(os.path.dirname(__file__), "assets", "img", "logo-mark.svg"), encoding="utf-8").read()

CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700&family=Unbounded:wght@600;700;800&display=swap');
*{box-sizing:border-box;margin:0}
html,body{background:#0b1426}
.card{--ink:#13213c;--blue:#1c4fd6;--yellow:#ffd23f;--muted:#9fb0cc;
  width:1200px;height:675px;position:relative;overflow:hidden;color:#fff;font-family:Onest,system-ui,sans-serif;
  background:radial-gradient(900px 520px at 12% -10%,rgba(28,79,214,.55),transparent 60%),
             radial-gradient(700px 420px at 105% 110%,rgba(255,210,63,.16),transparent 60%),#13213c}
.card::before{content:"";position:absolute;inset:0;opacity:.07;
  background:repeating-linear-gradient(115deg,#fff 0 2px,transparent 2px 46px)}
.card::after{content:"";position:absolute;left:0;right:0;bottom:0;height:12px;background:linear-gradient(90deg,var(--blue) 50%,var(--yellow) 50%)}
.top{position:absolute;left:64px;right:64px;top:48px;display:flex;align-items:center;justify-content:space-between;z-index:1}
.brand{display:flex;align-items:center;gap:16px}
.brand svg{width:60px;height:60px}
.brand b{display:block;font:800 30px/1 Unbounded,sans-serif;letter-spacing:-.01em}
.brand i{display:block;font:600 17px/1 Onest,sans-serif;font-style:normal;color:var(--yellow);letter-spacing:.32em;margin-top:6px}
.chip{font:700 22px/1 Unbounded,sans-serif;color:var(--ink);background:var(--yellow);padding:13px 24px;border-radius:999px}
.foot{position:absolute;left:64px;right:64px;bottom:44px;display:flex;justify-content:space-between;align-items:flex-end;z-index:1;font:600 26px/1.2 Onest,sans-serif;color:var(--muted)}
.foot strong{color:#fff;font-weight:700}
/* матч */
.match{position:absolute;left:64px;right:64px;top:180px;height:360px;display:grid;grid-template-columns:1fr 360px 1fr;align-items:center;z-index:1}
.team{display:flex;flex-direction:column;align-items:center;gap:22px;text-align:center}
.crest{width:176px;height:176px;border-radius:50%;background:#fff;display:grid;place-items:center;box-shadow:0 18px 40px rgba(0,0,0,.35)}
.crest img{width:140px;height:140px;object-fit:contain}
.crest span{font:800 54px/1 Unbounded,sans-serif;color:var(--c,#13213c)}
.tname{font:700 34px/1.15 Unbounded,sans-serif;max-width:330px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.mid{text-align:center}
.score{font:800 148px/1 Unbounded,sans-serif;letter-spacing:-.04em}
.time{font:800 112px/1 Unbounded,sans-serif;letter-spacing:-.03em;color:var(--yellow)}
.sub{margin-top:16px;font:600 26px/1.2 Onest,sans-serif;color:var(--muted)}
/* заголовкові картки */
.title{position:absolute;left:64px;right:64px;top:168px;z-index:1;font:800 66px/1.08 Unbounded,sans-serif;letter-spacing:-.02em;max-width:1000px}
.title em{font-style:normal;color:var(--yellow)}
.tiles{position:absolute;left:64px;right:64px;top:370px;display:grid;grid-template-columns:repeat(3,1fr);gap:24px;z-index:1}
.tile{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);border-radius:22px;padding:24px 28px}
.tile b{display:block;font:800 74px/1 Unbounded,sans-serif;color:var(--yellow)}
.tile span{display:block;margin-top:12px;font:600 24px/1.25 Onest,sans-serif;color:#dbe3f0}
.tv{position:absolute;left:64px;right:64px;top:300px;z-index:1;display:grid;gap:12px}
.tv div{display:grid;grid-template-columns:230px 1fr auto;align-items:center;gap:20px;background:rgba(255,255,255,.07);border-radius:16px;padding:14px 22px}
.tv b{font:700 28px/1 Unbounded,sans-serif;color:var(--yellow);white-space:nowrap}
.tv span{font:600 30px/1.1 Onest,sans-serif}
.tv i{font:700 20px/1 Onest,sans-serif;font-style:normal;background:#fff;color:var(--ink);padding:9px 14px;border-radius:999px}
.tv .tvq{background:transparent;color:var(--muted);border:1px solid rgba(255,255,255,.3)}
/* рубрика */
.rubric .big{position:absolute;left:64px;top:220px;z-index:1;font:800 104px/1.02 Unbounded,sans-serif;letter-spacing:-.03em;max-width:900px}
.rubric .lead{position:absolute;left:64px;top:470px;z-index:1;font:600 30px/1.3 Onest,sans-serif;color:#dbe3f0;max-width:760px}
.rubric .ghost{position:absolute;right:-170px;top:70px;width:600px;height:600px;opacity:.1;z-index:0}
.rubric .ghost svg{width:100%;height:100%}
"""

def brand(chip=None):
    c = f'<span class="chip">{E(chip)}</span>' if chip else ''
    return f'<div class="top"><div class="brand">{MARK}<div><b>ФУТБОЛ</b><i>УКРАЇНИ</i></div></div>{c}</div>'

def foot(left, right="ukrainianfootball.com.ua"):
    return f'<div class="foot"><span>{left}</span><span><strong>{E(right)}</strong></span></div>'

def crest(name, color):
    # У продакшені: <img src="{team.image_path}" alt=""> з API Sportmonks
    ini = "".join(w[0] for w in name.split()[:2]).upper()
    return f'<div class="crest" data-source="api:team.image_path"><span style="--c:{color}">{E(ini)}</span></div>'

def page(title, body):
    return f'<!doctype html><html lang="uk"><head><meta charset="utf-8"><title>{E(title)}</title><link rel="stylesheet" href="card.css"></head><body>{body}</body></html>'

CARDS = {
 "report": ("Картка звіту", f'''<div class="card">{brand("Звіт")}
  <div class="match"><div class="team">{crest("Шахтар","#e87a1e")}<div class="tname">Шахтар</div></div>
   <div class="mid"><div class="score">2:1</div><div class="sub">Фінальний свисток</div></div>
   <div class="team">{crest("Динамо","#1c4fd6")}<div class="tname">Динамо</div></div></div>
  {foot("УПЛ · 14-й тур · 15.11.2026")}</div>'''),
 "preview": ("Картка прев'ю", f'''<div class="card">{brand("Прев'ю")}
  <div class="match"><div class="team">{crest("Полісся","#1f8a4c")}<div class="tname">Полісся</div></div>
   <div class="mid"><div class="time">19:45</div><div class="sub">22 листопада · Житомир</div></div>
   <div class="team">{crest("Лівий Берег","#7a3fd1")}<div class="tname">Лівий Берег</div></div></div>
  {foot("Кубок України · 1/8 фіналу")}</div>'''),
 "round-stats": ("Картка підсумків туру", f'''<div class="card">{brand("Статистика")}
  <div class="title">14-й тур УПЛ<br><em>у цифрах</em></div>
  <div class="tiles"><div class="tile"><b>23</b><span>голи за тур</span></div><div class="tile"><b>2,88</b><span>голу в середньому за матч</span></div><div class="tile"><b>4:0</b><span>найбільша перемога туру</span></div></div>
  {foot("УПЛ · сезон 2026/27")}</div>'''),
 "tv-round": ("Картка «Де дивитися»", f'''<div class="card">{brand("Трансляції")}
  <div class="title" style="font-size:56px;top:160px">Де дивитися <em>15-й тур УПЛ</em></div>
  <div class="tv"><div><b>Пт 13:00</b><span>Зоря — Верес</span><i>UPL.TV</i></div><div><b>Сб 15:30</b><span>Шахтар — Динамо</span><i>UPL.TV</i></div><div><b>Нд 18:00</b><span>Полісся — Кривбас</span><i class="tvq">уточнюємо</i></div></div>
  {foot("Розклад трансляцій · час київський")}</div>'''),
}
RUBRICS = [("upl","УПЛ","Новини, таблиця і календар Прем'єр-ліги"),("persha-liga","Перша ліга","Новини, таблиця і календар Першої ліги"),
  ("druga-liga","Друга ліга","Новини, таблиці груп і календар Другої ліги"),("transfery-ukrayiny","Трансфери","Переходи і чутки українського футболу"),
  ("zbirna-ukrayiny","Збірна України","Матчі, склад і новини національної команди"),("kubok-ukrayiny","Кубок України","Пари, результати і новини турніру"),
  ("yevrokubky","Єврокубки","Українські клуби в ЛЧ, ЛЄ і ЛК"),("legionery","Легіонери","Українці в закордонних клубах"),
  ("statystyka","Статистика","Цифри, рекорди і бомбардири"),("korotko","Коротко","Головне за день у кількох рядках"),
  ("molod","Молодь","U-19 і молодіжна збірна U-21"),("translyacziyi","Де дивитися","Розклад трансляцій матчів")]

open(os.path.join(OUT, "card.css"), "w", encoding="utf-8").write(CSS)
for slug, (t, body) in CARDS.items():
    open(os.path.join(OUT, f"{slug}.html"), "w", encoding="utf-8").write(page(t, body))
for slug, name, lead in RUBRICS:
    body = f'<div class="card rubric">{brand()}<div class="ghost">{MARK}</div><div class="big"{' style="font-size:86px"' if len(name) > 10 else ''}>{E(name)}</div><div class="lead">{E(lead)}</div>{foot("Розділ сайту")}</div>'
    open(os.path.join(OUT, "rubrics", f"{slug}.html"), "w", encoding="utf-8").write(page(name, body).replace('href="card.css"', 'href="../card.css"'))

# галерея для розробників
items = "".join(f'<figure><img src="{s}.png" alt="{E(t)}" loading="lazy"><figcaption><b>{E(t)}</b> · <a href="{s}.html">HTML-шаблон</a> · <code>{s}</code></figcaption></figure>' for s, (t, _) in CARDS.items())
rub = "".join(f'<figure><img src="rubrics/{s}.png" alt="{E(n)}" loading="lazy"><figcaption><b>{E(n)}</b> · <a href="rubrics/{s}.png" download>PNG</a> · <code>{s}</code></figcaption></figure>' for s, n, _ in RUBRICS)
gallery = f'''<!doctype html><html lang="uk"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Картинки статей</title>
<style>body{{margin:0;background:#eef2f7;color:#13213c;font:16px/1.5 system-ui,sans-serif}}main{{max-width:1240px;margin:0 auto;padding:32px 16px}}h1{{margin:0 0 8px}}h2{{margin:40px 0 8px}}
p{{max-width:820px}}.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:20px}}figure{{margin:0;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(19,33,60,.08)}}
img{{display:block;width:100%;height:auto}}figcaption{{padding:10px 14px;font-size:14px}}code{{background:#eef2f7;padding:1px 6px;border-radius:4px}}a{{color:#1c4fd6}}</style></head><body><main>
<h1>Картинки для статей</h1>
<p>Розмір 1200×675 (16:9), PNG або WebP. Підходить для мініатюри статті, Open Graph і Google Discover (ширина від 1200 px).</p>
<h2>Картки, які сайт генерує автоматично</h2>
<p>Генерує сайт на запит агента (<code>POST /wp-json/uf/v1/agent/card</code>) або під час збереження статті з <code>uf_fixture_id</code>. Кружечки з літерами — заглушки: у продакшені там емблеми клубів з API Sportmonks (<code>team.image_path</code>).</p>
<div class="g">{items}</div>
<h2>Типові картинки рубрик</h2>
<p>Ставляться, якщо в статті немає своєї картинки і картку згенерувати неможливо. Завантажте у Медіафайли й призначте кожній рубриці.</p>
<div class="g">{rub}</div>
</main></body></html>'''
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(gallery)
print("ok", len(CARDS), len(RUBRICS))
