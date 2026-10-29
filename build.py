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
bg,fg,muted,gold,blue,grid='#0b1523','#f3f5fa','#b7c4d5','#f1c75b','#80bce9','#2e3d50'
image=Image.new('RGB',(1000,1060),bg)
draw=ImageDraw.Draw(image)
def font(size,bold=False):
    candidates = [Path('C:/Windows/Fonts')/('arialbd.ttf' if bold else 'arial.ttf'),Path('/usr/share/fonts/truetype/dejavu')/('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')]
    for candidate in candidates:
        if candidate.exists(): return ImageFont.truetype(str(candidate),size)
    return ImageFont.load_default(size=size)
def text(x,y,value,size=24,color=fg,bold=False,anchor=None):
    draw.text((x,y),value,fill=color,font=font(size,bold),anchor=anchor)
def number(value,decimals=2):
    return f'{value:,.{decimals}f}'.replace(',',' ').replace('.',',')
dates=[datetime.fromisoformat(d['date']) for d in rows]
values=[d['value_gold'] for d in rows]
latest=rows[-1];first=rows[0];change=latest['value_gold']-first['value_gold']
left,right,top,bottom=105,950,360,730
low,high=min(values)-180,max(values)+330
def x(d): return left+16+(d-dates[0]).days/max(1,(dates[-1]-dates[0]).days)*(right-left-32)
def y(value): return bottom-(value-low)/(high-low)*(bottom-top)
text(42,28,'PAG',44,gold,True)
text(155,43,'POLISH ARMAMENTS GROUP',29,gold,True)
text(42,94,'Wartość aktywów',29,fg,True)
text(42,136,dates[0].strftime('%d.%m')+'–'+dates[-1].strftime('%d.%m.%Y'),24,muted)
text(958,102,number(latest['value_gold'])+' G',47,fg,True,anchor='rt')
text(958,158,'Odczyt '+dates[-1].strftime('%d.%m.%Y'),22,muted,anchor='rt')
draw.line((42,210,958,210),fill=grid,width=2)
text(42,232,'+'+number(change)+' Gold',32,fg,True)
text(42,278,'Zmiana od '+dates[0].strftime('%d.%m'),23,muted)
text(958,232,'+'+number(change/first['value_gold']*100)+'%',36,gold,True,anchor='rt')
text(958,280,'Zmiana wartości aktywów',23,muted,anchor='rt')
text(left,328,'Gold',23,muted)
for value in range(((int(low)+499)//500)*500,int(high),500):
    py=y(value);draw.line((left,py,right,py),fill=grid,width=1);text(left-18,py,number(value,0),24,muted,anchor='rm')
for i,d in enumerate(rows):
    px=x(dates[i]);py=y(values[i]);status=d.get('status','confirmed')
    if i and (dates[i]-dates[i-1]).days==1 and all(rows[j].get('status') not in ('estimated_missing_day','saved_ui_refresh_unverified') for j in (i-1,i)):
        draw.line((x(dates[i-1]),y(values[i-1]),px,py),fill=gold,width=4)
    if status=='saved_ui_refresh_unverified': draw.rectangle((px-7,py-7,px+7,py+7),fill=blue)
    else: draw.ellipse((px-6,py-6,px+6,py+6),fill=bg if status=='estimated_missing_day' else gold,outline=gold,width=3)
    if i==len(rows)-1:
        draw.ellipse((px-8,py-8,px+8,py+8),fill=gold)
    elif d['date'] in (rows[0]['date'],'2026-10-17','2026-10-21'):
        text(px,py-27,number(values[i],0),24,fg,True,anchor='mm')
tick_indexes=sorted(set([0, min(4,len(rows)-1),min(8,len(rows)-1),min(13,len(rows)-1),len(rows)-1]))
for i in tick_indexes:
    text(x(dates[i]),752,dates[i].strftime('%d.%m'),24,muted,anchor='mt')
text(42,804,'● Odczyt    ○ Szacunek: 10 i 12.10',22,muted)
text(42,838,'■ 22.10: zapis UI, odświeżenie niezweryfikowane',22,muted)
draw.line((42,884,958,884),fill=grid,width=2)
metrics=[(42,number(latest['shares'],0),'akcji'),(290,str(latest['factories']),'fabryk'),(515,number(100*latest['leandro_shares']/latest['shares'])+'%','udział Leandro'),(785,number(latest['value_gold']/latest['shares'],2)+' G','na akcję')]
for px,value,label in metrics:
    text(px,904,value,32,fg,True)
    text(px,946,label,22,muted)
text(42,1001,'Wycena aktywów, nie zysk. Brak pomiarów 23–27.10.',22,muted)
image.save(ROOT/'pag-chart.tmp.png')
os.replace(ROOT/'pag-chart.tmp.png',ROOT/'pag-chart.png')
print(json.dumps({'records':len(rows),'latest':latest['date'],'value':latest['value_gold'],'dimensions':image.size},ensure_ascii=False))
