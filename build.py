"""Rebuild PAG outputs from history.json. Dependency: Pillow."""
import json
import os
from html import escape
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
history = json.loads((ROOT / 'history.json').read_text(encoding='utf-8'))
rows = history['observations']
assert len({(d['date'],d.get('observed_at')) for d in rows}) == len(rows)
assert rows == sorted(rows,key=lambda d:d['date'])
fragment = (ROOT / 'pag-template.html').read_text(encoding='utf-8').replace('__PAG_HISTORY__',json.dumps(history,ensure_ascii=False))
previous_fragment=(ROOT / 'pag-growth.html').read_text(encoding='utf-8') if (ROOT / 'pag-growth.html').exists() else None
def atomic_text(path, text):
    temporary=path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(text,encoding='utf-8')
    if temporary.read_text(encoding='utf-8')!=text: raise OSError('Write verification failed')
    os.replace(temporary,path)
if (ROOT / 'pag-chart.html').exists() and previous_fragment is not None:
    exported=(ROOT / 'pag-chart.html').read_text(encoding='utf-8')
    if escape(previous_fragment) not in exported: raise ValueError('Cannot locate previous fragment in HTML export')
    atomic_text(ROOT / 'pag-chart.html',exported.replace(escape(previous_fragment),escape(fragment)))
atomic_text(ROOT / 'pag-growth.html',fragment)
bg,fg,muted,gold,blue,grid='#0b1523','#f3f5fa','#aab8cb','#f1c75b','#80bce9','#2e3d50'
image=Image.new('RGB',(1600,1000),bg)
draw=ImageDraw.Draw(image)
def font(size,bold=False):
    candidates = [Path('C:/Windows/Fonts')/('arialbd.ttf' if bold else 'arial.ttf'),Path('/usr/share/fonts/truetype/dejavu')/('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')]
    for candidate in candidates:
        if candidate.exists(): return ImageFont.truetype(str(candidate),size)
    return ImageFont.load_default(size=size)
def text(x,y,value,size=18,color=fg,bold=False,anchor=None):
    draw.text((x,y),value,fill=color,font=font(size,bold),anchor=anchor)
dates=[datetime.fromisoformat(d['date']) for d in rows]
values=[d['value_gold'] for d in rows]
low,high=min(values)-160,max(values)+260
left,right,top,bottom=110,1540,290,780
def x(d): return left+14+(d-dates[0]).days/(dates[-1]-dates[0]).days*(right-left-28)
def y(value): return bottom-(value-low)/(high-low)*(bottom-top)
for value in range(2600,int(high),400):
    py=y(value);draw.line((left,py,right,py),fill=grid,width=1);text(left-22,py,f'{value:,}',19,muted,anchor='rm')
for i,d in enumerate(rows):
    px=x(dates[i]);py=y(values[i]);status=d.get('status','confirmed')
    if i and (dates[i]-dates[i-1]).days==1 and all(rows[j].get('status') not in ('estimated_missing_day','saved_ui_refresh_unverified') for j in (i-1,i)):
        draw.line((x(dates[i-1]),y(values[i-1]),px,py),fill=gold,width=4)
    if status=='saved_ui_refresh_unverified': draw.rectangle((px-7,py-7,px+7,py+7),fill=blue)
    else: draw.ellipse((px-6,py-6,px+6,py+6),fill=bg if status=='estimated_missing_day' else gold,outline=gold,width=3)
    text(px if i<len(rows)-1 else px-5,py+(22 if i%2 else -23),f'{values[i]:,.2f}',14,fg,True,anchor='ra' if i==len(rows)-1 else 'mm')
    text(px,805,d['date'][8:10]+'.'+d['date'][5:7],17,muted,True,anchor='mt')
latest=rows[-1];first=rows[0];change=latest['value_gold']-first['value_gold']
text(46,30,'PAG / POLISH ARMAMENTS GROUP',33,gold,True)
text(46,82,'ROZWÓJ WARTOŚCI AKTYWÓW',25,fg,True)
text(46,120,f"{rows[0]['date']} → {rows[-1]['date']}",19,muted)
text(1540,43,f"{latest['value_gold']:,.2f}",49,fg,True,anchor='rt')
text(1540,104,'GOLD · ODCZYT Z '+latest['date'],17,gold,True,anchor='rt')
text(46,181,f'+{change:,.2f} Gold / +{change/first["value_gold"]*100:.2f}% od 9.10',25,fg,True)
text(875,187,'200 Gold · dywidenda 13.10 (według raportu)',19,gold)
draw.line((46,240,1550,240),fill=grid,width=1)
text(110,263,'Szacowana wartość aktywów · Gold',16,muted)
text(1540,843,'Data · 2026',16,muted,anchor='rt')
text(46,870,'● Odczyt według źródła     ○ Szacunek: 10 i 12.10     ■ Zapis UI: 22.10, odświeżenie niezweryfikowane',17,muted)
draw.line((46,909,1550,909),fill=grid,width=1)
text(46,928,f"{latest['shares']} AKCJI       {latest['factories']} FABRYK       {latest['leandro_shares']} AKCJI LEANDRO ({100*latest['leandro_shares']/latest['shares']:.2f}%)       {latest['value_gold']/latest['shares']:.4f} GOLD / AKCJĘ",20,fg,True)
text(46,970,'Wartość obejmuje przepływy kapitału i ceny aktywów; nie jest zyskiem. Brak odczytów 23–27.10.',16,muted)
image.save(ROOT/'pag-chart.tmp.png')
os.replace(ROOT/'pag-chart.tmp.png',ROOT/'pag-chart.png')
print(json.dumps({'records':len(rows),'estimates':sum(d.get('status')=='estimated_missing_day' for d in rows),'latest':latest['date'],'value':latest['value_gold'],'growth_since_9_oct':change},ensure_ascii=False))
