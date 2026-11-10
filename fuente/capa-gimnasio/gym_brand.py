def gym_brand(h,nc=False):
    # V27.1 · gym = «Mi Gimnasio» (demo genérica, naranja deportivo) · nc = «Movimiento Inteligente» de Nahuel Cornu (logo propio, turquesa).
    # Nada de Almacén RAVE. Los créditos de Vincular Business no se tocan.
    if nc:
        NM,NMU,TAG,c1,c2,c3,lt='Movimiento Inteligente','MOVIMIENTO INTELIGENTE','NAHUEL CORNU','#060b21','#3de0c5','#1fb5a0','#3de0c5'
        LOC='Entrenamiento personalizado · Nahuel Cornu · Salta'
        lg='assets/nc-logo.jpeg'
        uri='data:image/jpeg;base64,'+base64.b64encode(open(lg,'rb').read()).decode()
    else:
        NM,NMU,TAG,c1,c2,c3,lt='Mi Gimnasio','MI GIMNASIO','DEMO','#111827','#f97316','#c2410c','#fb923c'
        LOC='Mi Gimnasio · demo'
        svg='<svg xmlns="http://www.w3.org/2000/svg" width="320" height="180" viewBox="0 0 320 180"><rect width="320" height="180" rx="22" fill="%s"/><g fill="%s"><rect x="44" y="70" width="16" height="40" rx="4"/><rect x="62" y="58" width="12" height="64" rx="4"/><rect x="246" y="58" width="12" height="64" rx="4"/><rect x="260" y="70" width="16" height="40" rx="4"/><rect x="74" y="85" width="172" height="10" rx="5"/></g><text x="160" y="78" font-family="Arial,Helvetica,sans-serif" font-size="34" font-weight="700" fill="#ffffff" text-anchor="middle">MI GIMNASIO</text><text x="160" y="140" font-family="Arial,Helvetica,sans-serif" font-size="20" letter-spacing="4" fill="%s" text-anchor="middle">DEMO</text></svg>'%(c1,c2,lt)
        uri='data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
    h=re.sub(r'const LOGO_MENU="[^"]*"','const LOGO_MENU="%s"'%uri,h,count=1)
    h=re.sub(r'const LOGO_TICKET="[^"]*"','const LOGO_TICKET="%s"'%uri,h,count=1)
    h=h.replace('--ink:#242220;','--ink:%s;'%c1,1).replace('--gold:#c9963e;','--gold:%s;'%c2,1).replace('--gold2:#a87a28;','--gold2:%s;'%c3,1)
    h=h.replace('style="width:48px;height:27px;object-fit:cover;border-radius:6px"','style="width:40px;height:40px;object-fit:%s;border-radius:8px"'%('cover' if nc else 'contain'))
    h=h.replace('Sistema RAVE','Sistema VB').replace('alt="RAVE"','alt="%s"'%NM)
    h=re.sub(r'<title>[^<]*</title>','<title>%s · %s</title>'%(NM,'Entrenamiento personalizado · Nahuel Cornu' if nc else 'Sistema VB para gimnasios · demo'),h,count=1)
    h=re.sub(r'(class=\\"logo\\" src=\\")data:image/[a-z]+;base64,[A-Za-z0-9+/=]+',lambda m:m.group(1)+uri,h,count=1)
    for o,n in [('Almacén y Licorería RAVE, Urquiza 1052, Salta, Argentina. Contacto: WhatsApp 387 4574892.','%s%s.'%(NM,' · Nahuel Cornu, Salta' if nc else ' (demo de evaluación, datos de ejemplo)')),
                ('Almacén y Licorería · Urquiza 1052 · Salta, Argentina',LOC),
                ('Mirá el menú de Almacén y Licorería RAVE (Urquiza 1052, Salta): vinos, bebidas, cigarrillos y combos. Pedí por WhatsApp 👇','Mirá los planes de %s. Consultas por WhatsApp 👇'%NM),
                ('Check out the menu of Almacén y Licorería RAVE (Urquiza 1052, Salta): wines, drinks, cigarettes and combos. Order via WhatsApp 👇','Check out the %s plans. Questions via WhatsApp 👇'%NM),
                ('Almacén y Licorería RAVE',NM),('Almacén y Licorería · Salta',LOC),('RAVE DIGITAL',NMU),('Club RAVE','Club '+NM),('class=\\"foot-brand\\">RAVE<','class=\\"foot-brand\\">%s<'%NMU),('alt=\\"RAVE','alt=\\"'+NM),('que RAVE guarde','que %s guarde'%NM),('RAVE Club',NM+' Club'),('<title>RAVE','<title>'+NM),
                ('Este menú incluye bebidas alcohólicas y tabaco.',''),('This menu includes alcoholic beverages and tobacco.','')]:
        h=h.replace(o,n)
    h=h.replace('--gold:#c9963e','--gold:%s'%c2).replace('--gold-deep:#dba854','--gold-deep:%s'%c2)
    h=h.replace('#side a.on{background:var(--gold);color:#1b1100;','#side a.on{background:var(--gold);color:#000;',1)
    h=h.replace('</style>','.btn.gold,.fk.gold,.fk.gold small,.cmp .btn.gold,html[data-theme=dark] .btn.gold,html[data-theme=dark] .fk.gold,html[data-theme=dark] .fk.gold small{color:#000!important}html[data-theme=dark] .cmp-tab.on{color:%s}html[data-theme=dark]{--gold2:%s}\n'%(lt,lt)+GYM_CSS+'\n</style>',1)
    if nc:
        # sistema del cliente: sin rótulos de «demo de evaluación» en la barra superior ni en el ingreso
        h=h.replace("'<span class=\"demo-b\">DEMO DE EVALUACIÓN</span>'","''")
        h=h.replace('Demo de evaluación. Usuarios de prueba:','Usuarios iniciales (cambiá los PIN en Usuarios y permisos):')
    return h
GYM_CSS='''.g-idle{border:2px dashed var(--line,#ccc);border-radius:14px;padding:1.2rem;text-align:center;display:flex;flex-direction:column;gap:.3rem}
.g-gate{border-radius:14px;padding:1rem 1.1rem;border:2px solid}.g-gate.ok{background:var(--okbg);border-color:var(--ok);color:var(--ok)}.g-gate.warn{background:var(--warnbg);border-color:#c98a00;color:#8a5a00}.g-gate.bad{background:var(--redbg);border-color:var(--red);color:var(--red)}.g-gate.mute{border-color:var(--line,#ccc)}
html[data-theme=dark] .g-gate.warn{color:#f3c76a}.g-gt{font-weight:800;letter-spacing:.08em;font-size:.85rem}.g-gn{font:700 1.6rem Georgia,serif;color:var(--ink-t,inherit)}.g-gate ul{margin:.4rem 0 0;padding-left:1.1rem}
.g-meter{height:8px;border-radius:99px;background:rgba(127,127,127,.2);overflow:hidden;margin:.3rem 0}.g-meter i{display:block;height:100%;background:var(--gold)}.g-meter.full i{background:var(--red)}
.g-days{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:.8rem;margin-bottom:1rem}.g-cls{border-top:1px solid rgba(127,127,127,.2);padding:.5rem 0;display:flex;flex-direction:column;gap:.25rem}
.g-bars{display:grid;grid-template-columns:repeat(8,1fr);gap:.4rem;align-items:end;height:130px}.g-bars div{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;font-size:.72rem;gap:.15rem}.g-bars i{display:block;width:70%;background:var(--gold);border-radius:6px 6px 0 0;min-height:2px}
.g-kiosk{position:fixed;inset:0;z-index:9000;background:var(--bg,#fff);overflow:auto;padding:1.2rem}.g-kin{max-width:860px;margin:0 auto;display:flex;flex-direction:column;gap:1rem}.g-clock{font:700 1.6rem Georgia,serif}'''
