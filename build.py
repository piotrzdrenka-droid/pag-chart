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
image=Image.new('RGB',(1600,900),bg)
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
left,right,top,bottom=105,1545,270,630
low,high=min(values)-180,max(values)+330
def x(d): return left+16+(d-dates[0]).days/max(1,(dates[-1]-dates[0]).days)*(right-left-32)
def y(value): return bottom-(value-low)/(high-low)*(bottom-top)
text(42,28,'PAG',44,gold,True)
text(155,43,'POLISH ARMAMENTS GROUP',29,gold,True)
text(42,94,'Wartość aktywów',29,fg,True)
text(42,132,dates[0].strftime('%d.%m')+'–'+dates[-1].strftime('%d.%m.%Y'),24,muted)
text(1558,102,number(latest['value_gold'])+' G',47,fg,True,anchor='rt')
text(1558,158,'Odczyt '+dates[-1].strftime('%d.%m.%Y'),22,muted,anchor='rt')
draw.line((42,188,1558,188),fill=grid,width=2)
text(42,206,'+'+number(change)+' Gold',32,fg,True)
text(460,215,'Zmiana od '+dates[0].strftime('%d.%m'),23,muted)
text(1558,206,'+'+number(change/first['value_gold']*100)+'%',36,gold,True,anchor='rt')
text(1165,215,'Zmiana wartości aktywów',23,muted,anchor='rt')
text(left,250,'Gold',23,muted)
for value in range(((int(low)+499)//500)*500,int(high),500):
    py=y(value);draw.line((left,py,right,py),fill=grid,width=1);text(left-18,py,number(value,0),24,muted,anchor='rm')
# Draw connectors before markers so they do not overpaint hollow points.
for i in range(1,len(rows)):
    draw.line((x(dates[i-1]),y(values[i-1]),x(dates[i]),y(values[i])),fill=gold,width=4)
occupied=[]
for i,d in enumerate(rows):
    px=x(dates[i]);py=y(values[i]);status=d.get('status','confirmed')
    if status=='saved_ui_refresh_unverified': draw.rectangle((px-7,py-7,px+7,py+7),fill=blue)
    else: draw.ellipse((px-6,py-6,px+6,py+6),fill=bg if status=='estimated_missing_day' else gold,outline=gold,width=3)
    if i==len(rows)-1: draw.ellipse((px-8,py-8,px+8,py+8),fill=gold)
    label=number(values[i])
    label_font=font(24,True)
    width=draw.textbbox((0,0),label,font=label_font)[2]
    lx=min(max(px,left+width/2+2),right-width/2-2)
    options=[sign*offset for offset in range(30,285,32) for sign in ((-1,1) if i%2==0 else (1,-1))]
    for offset in options:
        ly=py+offset
        rect=(lx-width/2-5,ly-16,lx+width/2+5,ly+16)
        if rect[1]<top-10 or rect[3]>bottom+16: continue
        if not any(rect[0]<r[2]+8 and rect[2]>r[0]-8 and rect[1]<r[3]+8 and rect[3]>r[1]-8 for r in occupied):
            break
    else: raise ValueError('No non-overlapping position for '+d['date'])
    occupied.append(rect)
    if abs(offset)>35: draw.line((px,py,lx,ly+(16 if offset<0 else -16)),fill=muted,width=1)
    draw.rectangle(rect,fill=bg)
    text(lx,ly,label,24,fg,True,anchor='mm')
tick_indexes=sorted(set([0, min(4,len(rows)-1),min(8,len(rows)-1),min(13,len(rows)-1),len(rows)-1]))
for i in tick_indexes:
    text(x(dates[i]),660,dates[i].strftime('%d.%m'),24,muted,anchor='mt')
text(42,705,'● Odczyt    ○ Szacunek: 10 i 12.10',22,muted)
text(685,705,'■ 22.10: zapis UI, odświeżenie niezweryfikowane',22,muted)
draw.line((42,750,1558,750),fill=grid,width=2)
metrics=[(42,number(latest['shares'],0),'akcji'),(430,str(latest['factories']),'fabryk'),(785,number(100*latest['leandro_shares']/latest['shares'])+'%','udział Leandro'),(1235,number(latest['value_gold']/latest['shares'],2)+' G','na akcję')]
for px,value,label in metrics:
    text(px,767,value,32,fg,True)
    text(px,810,label,22,muted)
text(42,857,'Linia łączy zapisy; brak pomiarów 23–27.10.',22,muted)
text(1000,857,'Wycena aktywów, nie zysk.',22,muted)
image.save(ROOT/'pag-chart.tmp.png')
os.replace(ROOT/'pag-chart.tmp.png',ROOT/'pag-chart.png')
print(json.dumps({'records':len(rows),'latest':latest['date'],'value':latest['value_gold'],'dimensions':image.size},ensure_ascii=False))
