from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
root=Path(__file__).resolve().parent
im=Image.new('RGB',(1200,650),'#0b1523');d=ImageDraw.Draw(im)
def t(x,y,s,size=28,c='#f3f5fa',bold=False):
 f=ImageFont.truetype('C:/Windows/Fonts/'+('arialbd.ttf' if bold else 'arial.ttf'),size);d.text((x,y),s,font=f,fill=c)
t(40,25,'PAG / DIVIDEND UPDATE',38,'#f1c75b',True)
t(40,80,'30.10.2026 · potwierdzone wypłaty / confirmed payments',25,'#b7c4d5')
t(40,132,'275 GOLD',64,'#f1c75b',True)
t(650,145,'475 GOLD',48,'#f3f5fa',True)
t(650,205,'13.10 + 30.10 · dwie opisane rundy',24,'#b7c4d5')
t(40,215,'Dziś / Today',25,'#b7c4d5')
d.line((40,265,1160,265),fill='#2e3d50',width=2)
for x,amount,time in [(40,'75 G','01:20:30'),(330,'75 G','01:25:31'),(620,'100 G','01:35:32'),(910,'25 G','02:35:33')]:
 t(x,285,amount,38,'#f1c75b',True);t(x,338,time,26,'#b7c4d5')
t(40,393,'Dywidendy / Dividends · Gold',25,'#b7c4d5')
for y,label,value in [(440,'13.10',200),(510,'30.10',275)]:
 t(40,y+4,label,28);d.rectangle((160,y,160+value*2.5,y+43),fill='#f1c75b');t(180+value*2.5,y+3,str(value)+' G',28,bold=True)
t(945,455,'+37,5%',36,'#f1c75b',True)
t(945,505,'vs 13.10',25,'#b7c4d5')
t(40,594,'Źródło / Source: logi PAG · 30.10.2026 · czas serwera / server time',23,'#b7c4d5')
im.save(root/'pag-dividends-2026-10-30.png')
