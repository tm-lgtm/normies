import json, re, html, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from meta import M, TOP, SERIES

SP = os.path.dirname(os.path.abspath(__file__)) + '/'
src = open('/home/user/normies/index.html').read()
css = src[src.find('<style>')+7:src.find('</style>')]
fonts = '\n'.join(re.findall(r'@font-face\{[^}]*\}', css))
_i = src.find('const CH = ') + len('const CH = ')
CH = json.JSONDecoder().raw_decode(src, _i)[0]
BY = {c['n']: c for c in CH}
e = html.escape

def stars(n):
    return '<span class="stars">' + '●'*n + '<span class="off">' + '●'*(5-n) + '</span></span>'

def belt(c):
    return c['belt']

def chip(c):
    b = belt(c)
    return f'<span class="chip" style="background:{b}"></span>'

def wc(c):
    return len(re.sub('<[^>]+>', ' ', c['html']).split())

def imgs(c):
    return len(re.findall('<img', c['html']))

# ---------- table ----------
rows = []
for c in CH:
    m = M[c['n']]
    rows.append(f'''<tr>
<td class="no">{c['n']:02d}</td>
<td class="tt"><b>{e(c['title'])}</b><div class="sub">{e(m['idea'])}</div></td>
<td>{chip(c)}{e(c['section'])}</td>
<td class="dt">{e(m['date'])}<div class="sub">{e(m['conf'])}</div></td>
<td>{e(' / '.join(m['fmt']))}</td>
<td>{e(', '.join(m['topics']))}</td>
<td class="yt">{stars(m['yt'])}</td>
</tr>''')
table = '\n'.join(rows)

# ---------- top picks ----------
top = []
for i, n in enumerate(TOP, 1):
    c, m = BY[n], M[n]
    top.append(f'''<div class="pick">
<div class="pk-h"><span class="rank">{i}</span><div><div class="eyebrow">{chip(c)}No. {n:02d} · {e(c['section'])} · {e(m['date'])}</div>
<div class="pk-t">{e(m['title'])}</div></div>{stars(m['yt'])}</div>
<div class="pk-row"><span class="k">Hook</span><span class="v hookv">“{e(m['hook'])}”</span></div>
<div class="pk-row"><span class="k">Format</span><span class="v">{e(m['vid'])}</span></div>
<div class="pk-row"><span class="k">Proof</span><span class="v">{e(m['assets'])}</span></div>
{f'<div class="pk-row flag"><span class="k">Note</span><span class="v">{e(m["flag"])}</span></div>' if m.get('flag') else ''}
</div>''')

# ---------- series ----------
ser = []
for name, ns in SERIES:
    items = ''.join(f'<li><span class="no">{n:02d}</span>{e(BY[n]["title"])} <span class="q">→ {e(M[n]["title"])}</span></li>' for n in ns)
    ser.append(f'<div class="series"><h3>{e(name)}</h3><ol>{items}</ol></div>')

# ---------- format mix ----------
from collections import Counter
fam = Counter()
FAM = [('Story', ['story','Story','Anecdote','Throwback','Confession','update','Update','recap','Tribute','observation']),
       ('Case study', ['Case study','case study','Case','case']),
       ('Framework / plan', ['Framework','framework','Plan','how-to','Sales letter','Thought experiment','Experiment']),
       ('Philosophy / manifesto', ['Philosophy','philosophy','Manifesto','Hot take','Metaphor','Contrarian'])]
for c in CH:
    got = set()
    for f in M[c['n']]['fmt']:
        for name, keys in FAM:
            if any(k in f for k in keys): got.add(name)
    for g in got: fam[g] += 1
ytc = Counter(M[n]['yt'] for n in M)

# ---------- archive ----------
arch = []
cur = None
secdesc = {}
for c in CH: secdesc.setdefault(c['part'], (c['section'], c['desc'], c['belt'], []))[3].append(c['n'])
for c in CH:
    if c['part'] != cur:
        cur = c['part']
        s = secdesc[cur]
        dark = s[2] in ('#000000', '#813682', '#0196FF', '#DE413C', '#51A44E')
        arch.append(f'''<section class="divider" style="background:{s[2]};color:{'#fff' if dark else '#0A0A0A'}; {'border:1.5px solid #0A0A0A;' if s[2]=='#FFFFFF' else ''}">
<div class="eyebrow" style="color:inherit;opacity:.7">Part {cur}</div><h2>{e(s[0])}</h2><div class="dd">{e(s[1])}</div>
<div class="dl">{''.join(f'<div><span>{n:02d}</span>{e(BY[n]["title"])}</div>' for n in s[3])}</div></section>''')
    m = M[c['n']]
    body = c['html'].replace('src="images/', 'src="file:///home/user/normies/images/')
    arch.append(f'''<article class="email">
<div class="beltline" style="background:{c['belt']};{'border-bottom:1px solid #0A0A0A;' if c['belt']=='#FFFFFF' else ''}"></div>
<div class="ehead"><div class="eyebrow">No. {c['n']:02d} · {e(c['section'])} · {wc(c)} words{f' · {imgs(c)} image' + ('s' if imgs(c)>1 else '') if imgs(c) else ''}</div>
<h1>{e(c['title'])}</h1></div>
<div class="meta">
 <div class="mrow"><span class="k">Est. date</span><span class="v"><b>{e(m['date'])}</b> <span class="conf">({e(m['conf'])} confidence)</span><br><span class="basis">{e(m['basis'])}</span></span></div>
 <div class="mrow"><span class="k">Email format</span><span class="v">{''.join(f'<span class="tag">{e(f)}</span>' for f in m['fmt'])}</span></div>
 <div class="mrow"><span class="k">Topics</span><span class="v">{''.join(f'<span class="tag t2">{e(t)}</span>' for t in m['topics'])}</span></div>
 <div class="mrow"><span class="k">Big idea</span><span class="v">{e(m['idea'])}</span></div>
 <div class="mrow"><span class="k">Proof & assets</span><span class="v">{e(m['assets'])}</span></div>
 <div class="yt-box">
  <div class="ythead"><span class="eyebrow">YouTube potential</span>{stars(m['yt'])}</div>
  <div class="mrow"><span class="k">Video format</span><span class="v">{e(m['vid'])}</span></div>
  <div class="mrow"><span class="k">Working title</span><span class="v"><b>{e(m['title'])}</b></span></div>
  <div class="mrow"><span class="k">Cold-open hook</span><span class="v hookv">“{e(m['hook'])}”</span></div>
  {f'<div class="mrow flag"><span class="k">Heads-up</span><span class="v">{e(m["flag"])}</span></div>' if m.get('flag') else ''}
 </div>
</div>
<div class="pbody">{body}</div>
</article>''')

doc = f'''<!doctype html><html><head><meta charset="utf-8"><title>Normies: Email Archive & YouTube Planner</title>
<style>
{fonts}
@page {{ size: A4; margin: 16mm 16mm 16mm 16mm; }}
:root{{--paper:#FBF8F1;--ink:#0A0A0A;--quiet:#6B6B6B;--rule:#D9D3C4;--marker:rgba(255,210,61,.82);}}
*{{box-sizing:border-box;margin:0;padding:0}}
html{{-webkit-print-color-adjust:exact;print-color-adjust:exact}}
body{{font-family:"Gotham","Helvetica Neue",Arial,sans-serif;font-weight:200;color:var(--ink);font-size:10pt;line-height:1.45}}
b,strong{{font-weight:500}}
.eyebrow{{font-weight:500;font-size:7.5pt;letter-spacing:.2em;text-transform:uppercase;color:var(--quiet)}}
.chip{{display:inline-block;width:8px;height:8px;border:1px solid rgba(0,0,0,.35);margin-right:5px;vertical-align:0}}
.stars{{color:#0A0A0A;letter-spacing:1px;font-size:8.5pt;white-space:nowrap}} .stars .off{{color:#D9D3C4}}
h2.pt{{font-weight:900;font-style:italic;font-size:24pt;letter-spacing:-.02em;line-height:1.05;margin:4px 0 10px}}
p.intro{{max-width:150mm;margin-bottom:10px}}
.page{{break-after:page}}
/* cover */
.cover{{background:#000;color:#fff;height:265mm;padding:22mm 16mm;display:flex;flex-direction:column;justify-content:space-between}}
.cover h1{{font-weight:900;font-style:italic;font-size:46pt;line-height:.98;letter-spacing:-.03em}}
.cover .sub{{font-size:15pt;margin-top:14px;font-weight:200}}
.cover .belts{{display:flex;height:8px;margin-top:22px}} .cover .belts span{{flex:1}}
.cover .facts{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;border-top:1px solid #444;padding-top:12px}}
.cover .facts b{{display:block;font-family:"Gotham X Narrow";font-weight:900;font-size:30pt;line-height:1}}
.cover .facts span{{font-size:8pt;letter-spacing:.15em;text-transform:uppercase;color:#aaa}}
/* legend */
.legend{{display:grid;grid-template-columns:1fr 1fr;gap:10px 18px;margin-top:10px}}
.legend .box{{border-top:1.5px solid var(--ink);padding-top:6px}}
.legend h4{{font-weight:500;font-size:9pt;margin-bottom:4px}}
.legend li{{margin-left:14px;font-size:8.8pt}}
.mix{{display:flex;gap:16px;margin:10px 0 4px}} .mix div{{flex:1;background:var(--paper);padding:8px 10px}}
.mix b{{font-family:"Gotham X Narrow";font-weight:900;font-size:22pt;display:block;line-height:1}}
.mix span{{font-size:7.5pt;letter-spacing:.12em;text-transform:uppercase;color:var(--quiet)}}
/* table */
table{{width:100%;border-collapse:collapse;font-size:7.6pt;line-height:1.3}}
th{{text-align:left;font-weight:500;font-size:6.8pt;letter-spacing:.14em;text-transform:uppercase;color:var(--quiet);border-bottom:1.5px solid var(--ink);padding:4px 4px}}
td{{border-bottom:1px solid var(--rule);padding:4px 4px;vertical-align:top}}
tr{{break-inside:avoid}} thead{{display:table-header-group}}
td.no{{font-family:"Gotham X Narrow";font-weight:900;font-size:11pt}}
td.tt{{width:34%}} td .sub{{color:var(--quiet);font-size:7pt;margin-top:1px}}
td.dt{{white-space:nowrap}}
/* picks */
.pick{{border-top:1.5px solid var(--ink);padding:7px 0 8px;break-inside:avoid}}
.pk-h{{display:flex;gap:10px;align-items:flex-start}} .pk-h>div{{flex:1}}
.rank{{font-family:"Gotham X Narrow";font-weight:900;font-size:24pt;line-height:.9;width:26px}}
.pk-t{{font-weight:900;font-style:italic;font-size:12.5pt;letter-spacing:-.01em;line-height:1.15;margin-top:2px}}
.pk-row,.mrow{{display:flex;gap:10px;font-size:8.6pt;margin-top:3px}}
.k{{flex:0 0 29mm;font-weight:500;font-size:6.8pt;letter-spacing:.14em;text-transform:uppercase;color:var(--quiet);padding-top:2px}}
.pk-row .k{{margin-left:36px;flex-basis:16mm}}
.v{{flex:1}} .hookv{{font-style:italic}}
.flag .v{{color:#B23A2E}}
/* series */
.series{{break-inside:avoid;margin-bottom:10px;border-top:1.5px solid var(--ink);padding-top:6px}}
.series h3{{font-weight:900;font-style:italic;font-size:12pt;margin-bottom:3px}}
.series ol{{list-style:none;font-size:8.6pt}} .series li{{padding:2px 0;border-bottom:1px solid var(--rule)}}
.series .no{{font-weight:500;display:inline-block;width:20px}} .series .q{{color:var(--quiet)}}
/* dividers */
.divider{{height:265mm;padding:24mm 16mm;break-before:page;break-after:page;display:flex;flex-direction:column;justify-content:center}}
.divider h2{{font-weight:900;font-style:italic;font-size:54pt;letter-spacing:-.03em;line-height:1}}
.divider .dd{{font-size:15pt;margin:8px 0 22px}}
.divider .dl div{{font-size:11pt;padding:4px 0;border-top:1px solid currentColor;opacity:.9}}
.divider .dl span{{font-weight:500;display:inline-block;width:30px}}
/* email */
.email{{break-before:page}}
.beltline{{height:6px;margin-bottom:10px}}
.ehead h1{{font-weight:900;font-style:italic;font-size:25pt;line-height:1.02;letter-spacing:-.025em;margin:4px 0 10px}}
.meta{{background:var(--paper);padding:10px 12px 10px;margin-bottom:14px;break-inside:avoid}}
.meta .mrow{{margin-top:4px}}
.conf{{color:var(--quiet)}} .basis{{color:var(--quiet);font-size:7.8pt}}
.tag{{display:inline-block;border:1px solid var(--ink);padding:0 5px;margin:0 4px 2px 0;font-size:7.6pt;font-weight:500}}
.tag.t2{{border-color:var(--rule);background:#fff;font-weight:200}}
.yt-box{{border-top:1px solid var(--rule);margin-top:8px;padding-top:6px}}
.ythead{{display:flex;justify-content:space-between;align-items:center}}
.pbody{{font-size:10.2pt;line-height:1.55;max-width:150mm}}
.pbody p{{margin-bottom:7px}}
.pbody .lead{{font-weight:500}}
.shout{{font-weight:900;font-style:italic;font-size:15pt;line-height:1.12;margin:10px 0;letter-spacing:-.01em}}
.whisper{{font-style:italic;font-size:15pt;line-height:1.2;margin:10px 0}}
.mutter{{font-family:"Verveine",cursive;text-transform:uppercase;font-size:10.5pt;display:inline-block;transform:rotate(-1.5deg);margin:0 0 8px}}
.callout{{font-family:"Verveine",cursive;text-transform:uppercase;font-size:13pt;line-height:1.3;display:inline-block;margin:6px 0 10px}}
.hl{{background-image:linear-gradient(transparent 12%,var(--marker) 12%,var(--marker) 94%,transparent 94%);padding:0 .1em}}
figure.fig{{margin:6px 0 10px;break-inside:avoid}}
figure.fig img{{display:block;max-width:100%;max-height:95mm;width:auto;height:auto}}
.fig-shot img{{border:1px solid var(--rule)}}
.fig-photo img{{background:#fff;padding:6px 6px 9px;box-shadow:0 1px 3px rgba(0,0,0,.2);max-height:80mm}}
figcaption{{display:none}}
</style></head><body>

<div class="cover page">
 <div><div class="eyebrow" style="color:#9b9b9b">Taki Moore · Email Archive · YouTube Planner</div>
 <h1 style="margin-top:14px">I Feel Sorry<br>for the Normies</h1>
 <div class="sub">49 of the best emails, tagged by topic, estimated date and format, with a YouTube angle for each one.</div>
 <div class="belts">{''.join(f'<span style="background:{secdesc[p][2]};{"outline:1px solid #555" if secdesc[p][2] in ("#000000",) else ""}"></span>' for p in sorted(secdesc))}</div></div>
 <div class="facts"><div><b>49</b><span>Emails</span></div><div><b>8</b><span>Sections</span></div><div><b>{sum(1 for n in M if M[n]['yt']>=5)}</b><span>Rated ●●●●● for YouTube</span></div><div><b>{sum(wc(c) for c in CH)//1000}K</b><span>Words</span></div></div>
</div>

<div class="page">
 <div class="eyebrow">How to use this</div>
 <h2 class="pt">Reading the tags</h2>
 <p class="intro">Every email has the same metadata block, followed by the full email. Start with the <b>Top picks</b> list, then use the <b>Playlists</b> page to group videos into series. Each email's YouTube block gives you a working title, a cold-open hook taken from the email itself, and a suggested video format.</p>
 <div class="legend">
  <div class="box"><h4>Estimated date</h4><ul>
   <li>The archive doesn't store send dates, so every date here is <b>inferred from clues in the email</b> (e.g. “no sales team since Christmas 2024… 14 months ago” puts No. 07 around Feb 2026).</li>
   <li><b>High</b>: a specific anchor in the text. <b>Medium</b>: a strong relative clue. <b>Low</b>: era and context only. <b>—</b>: evergreen, no clue.</li>
   <li>If you have the ESP export (ConvertKit, ActiveCampaign, etc.), swap in the real send dates.</li></ul></div>
  <div class="box"><h4>Email format</h4><ul>
   <li><b>Story</b>: personal, family, travel or comedy story → lesson.</li>
   <li><b>Case study</b>: a client's or your own business's before → after, with numbers.</li>
   <li><b>Framework / Plan</b>: a teachable model, maths or step-by-step.</li>
   <li><b>Philosophy</b>: manifesto, contrarian take, metaphor.</li>
   <li><b>Update / Confession</b>: behind the scenes, what changed and why.</li></ul></div>
  <div class="box"><h4>YouTube potential ●●●●●</h4><ul>
   <li><b>5</b>: strong hook + real numbers or a story + a teachable idea. Make it a long-form video.</li>
   <li><b>4</b>: solid, maybe better as a mid-length video or inside a bigger video.</li>
   <li><b>3</b>: best as a Short or a vlog segment.</li>
   <li><b>2</b>: personal; check with family first.</li></ul></div>
  <div class="box"><h4>Video formats used</h4><ul>
   <li><b>Story-led long-form</b>: open cold on the story, reveal the lesson at the midpoint.</li>
   <li><b>Whiteboard / brown-paper explainer</b>: your kraft-card frameworks on camera.</li>
   <li><b>Case-study breakdown</b>: numbers on screen, ideally with the client.</li>
   <li><b>Short (≤60s)</b>: one moment, one line.</li></ul></div>
 </div>
 <div class="eyebrow" style="margin-top:16px">Format mix across the 49</div>
 <div class="mix">{''.join(f'<div><b>{fam[k]}</b><span>{k}</span></div>' for k,_ in FAM)}</div>
 <div class="mix">{''.join(f'<div><b>{ytc[s]}</b><span>Rated {s}/5</span></div>' for s in (5,4,3,2))}</div>
 <p class="intro" style="margin-top:8px;color:var(--quiet);font-size:8.5pt">Emails can carry more than one format, so the format counts add up to more than 49.</p>
</div>

<div class="page">
 <div class="eyebrow">At a glance</div>
 <h2 class="pt">All 49 emails</h2>
 <table><thead><tr><th>#</th><th>Title · big idea</th><th>Section</th><th>Est. date</th><th>Format</th><th>Topics</th><th>YT</th></tr></thead>
 <tbody>{table}</tbody></table>
</div>

<div class="page">
 <div class="eyebrow">Shortlist</div>
 <h2 class="pt">Top {len(TOP)} picks for YouTube</h2>
 <p class="intro">Ranked by hook strength, hard numbers, how easy they are to show on camera, and how well they point to your offers (Salesless, Black Belt, Boardroom). Film 1–3 first. They have the widest appeal.</p>
 {''.join(top)}
</div>

<div class="page">
 <div class="eyebrow">Playlists</div>
 <h2 class="pt">Suggested series</h2>
 <p class="intro">Grey text is each video's working title. Lead each playlist with its first video, since that one has the strongest hook.</p>
 {''.join(ser)}
</div>

{''.join(arch)}
</body></html>'''
open(SP + 'normies-archive.html', 'w').write(doc)
print('ok', len(doc))
