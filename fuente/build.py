#!/usr/bin/env python3
"""Arma el index.html. Uso: python3 build.py demo|cliente [salida.html]
Variables de entorno (sólo cliente): SUPABASE_URL, SUPABASE_KEY (clave PUBLICABLE), RAVE_SLUG, PUBLIC_URL"""
import sys,os,json,subprocess,re
V=sys.argv[1] if len(sys.argv)>1 else 'demo'
assert V in('demo','cliente','kini','solo','v3','gym','nc')
# perfiles de demo (V26.43): kini = mayorista (KiniDistribuidoraDemo) · solo = comercio de un solo dueño (raveV2) · v3 = como Almacén RAVE con el equipo SVB R2AVE (raveV3)
PROFILE=V if V in('kini','solo','v3','gym','nc') else ''
KINI=V=='kini'
if PROFILE: V='demo'
out=sys.argv[2] if len(sys.argv)>2 else 'index.html'
B=lambda f:open(f,encoding='utf8').read()
subprocess.check_call(['python3','gen_data.py'],stdout=subprocess.DEVNULL);subprocess.check_call(['python3','assemble.py'],stdout=subprocess.DEVNULL)
url=os.environ.get('SUPABASE_URL','').rstrip('/');key=os.environ.get('SUPABASE_KEY','')
if V=='demo': url='';key=''
assert not re.search(r'service_role|sb_secret_',key),'¡Esa es una clave SECRETA! Usá la clave publicable (sb_publishable_…)'
if url: assert re.fullmatch(r'https://[A-Za-z0-9.-]+(:\d+)?',url),'URL inválida'
slug=os.environ.get('RAVE_SLUG','almacen-rave' if V=='cliente' else '')
pub=os.environ.get('PUBLIC_URL','https://raveholding.github.io/'+('AlmacenRAVE/' if V=='cliente' else 'raveV2/'))
import datetime
if KINI: pub=os.environ.get('PUBLIC_URL','https://raveholding.github.io/KiniDistribuidoraDemo/')
if PROFILE=='v3': pub=os.environ.get('PUBLIC_URL','https://raveholding.github.io/raveV3/')
# V27.1 · gym = demo genérica de gimnasios (SVBDemoGimnasios) · nc = entrenador personal Nahuel Cornu (MovimientoInteligenteNC)
if PROFILE=='gym': pub=os.environ.get('PUBLIC_URL','https://raveholding.github.io/SVBDemoGimnasios/')
if PROFILE=='nc': pub=os.environ.get('PUBLIC_URL','https://raveholding.github.io/MovimientoInteligenteNC/')
build={'ver':datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')+' UTC','variant':V,'db':'rave-almacenrave-v1' if V=='cliente' else {'kini':'rave-kini-demo-v2','solo':'rave-solo-demo-v1','v3':'rave-v3-demo-v2','gym':'rave-gym-demo-v1','nc':'rave-nc-mi-v1'}.get(PROFILE,'rave-cliente-v3'),'publicUrl':pub}
if PROFILE: build['profile']=PROFILE
cfg='<script>window.RAVE_BUILD=%s;window.RAVE_CLOUD=%s;</script>\n'%(json.dumps(build),json.dumps({'url':url,'key':key,'slug':slug}))
head=B('p1-head.html')
head=head.replace("connect-src 'none'","connect-src "+(url if url else "'none'"))
if V=='cliente':
    # SEO del menú público (V26.33): título, descripción, dirección canónica y datos del local para buscadores.
    # Reemplaza en Google la dirección vieja (raveholding.github.io/menu-rave) por la actual.
    seo_t='Almacén y Licorería RAVE · Menú digital · Salta'
    seo_d='Almacén y Licorería RAVE, Urquiza 1052, Salta, Argentina. Menú digital con precios, pedidos por WhatsApp (387 4574892) y Club RAVE.'
    ld={"@context":"https://schema.org","@type":"LiquorStore","name":"Almacén y Licorería RAVE","url":pub,"telephone":"+54 9 387 457 4892",
        "address":{"@type":"PostalAddress","streetAddress":"Urquiza 1052","addressLocality":"Salta","addressRegion":"Salta","addressCountry":"AR"}}
    seo=('<title>%s</title>\n<meta name="description" content="%s">\n<meta name="robots" content="index,follow">\n<link rel="canonical" href="%s">\n'
         '<meta property="og:type" content="website">\n<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n<meta property="og:url" content="%s">\n'
         '<meta property="og:locale" content="es_AR">\n<script type="application/ld+json">%s</script>')%(seo_t,seo_d,pub,seo_t,seo_d,pub,json.dumps(ld,ensure_ascii=False))
    head=head.replace('<title>Sistema RAVE · Almacén y Licorería RAVE — Demo</title>',seo)
head=head.replace('<style>',cfg+'<style>',1)
parts=['p2-core.js','p2b-sort.js','p2c-ux.js','p3-ops.js','p3b-pos.js','p3p-payadj.js','p3n-posquick.js','p3c-cash.js','p3q-cortes.js','p3f-transfers.js','p3g-paydetail.js','p3h-expediente.js','p3i-rubcash.js','p3j-combos.js','p3k-owner.js','p3l-kini.js','p3o-solo.js','p3m-payacc.js','p3d-assist.js','p3e-saledetail.js','p3r-oper.js','p6-loyalty.js','p6c-custadmin.js','p6d-cardportable.js','p6e-wallet.js','p6b-wholesale.js','p6f-credito.js','p6g-wacliente.js','p6h-fidel.js','p6i-fiscal.js','p6j-crm.js','p4-mods.js','p4f-rrhh.js','p4c-compras.js','p4d-compras-ui.js','p4e-factura.js','p4b-online.js','p7a-dash.js','p7b-charts.js','p7c-scale.js','p7-devices.js','p8-legal.js','p9-cloud.js','p9b-arca.js','p9c-tiendanube.js','p5c-menusec.js','p5b-store.js','p5d-cscreen.js','p5-menu-boot.js']
parts=[p for p in parts if os.path.exists(p)]
if PROFILE in('gym','nc'): parts.insert(parts.index('p5c-menusec.js'),'p11-gym.js')
# V26.37 · Centro Inteligente (p10-centro.js): módulo aislado.
# V26.40: aprobado por el dueño para Almacén RAVE (apagado por defecto; lo activa el administrador). Kini no lo lleva salvo CI=1.
# raveV2 (solo) y Kini no llevan el Centro Inteligente: es de raveV3 y de Almacén RAVE (apagado)
if (V in ('demo','cliente') and PROFILE not in('kini','solo','gym','nc')) or os.environ.get('CI')=='1': parts.append('p10-centro.js')
# V26.42 · Equipo SVB R2AVE (p10b-r2ave.js): extensión del Centro Inteligente SÓLO para la demo raveV2 hasta que el dueño
# apruebe la demostración. El cliente (Almacén RAVE) y Kini NO la llevan; con R2AVE=1 se fuerza (pruebas).
# V26.43: el equipo SVB R2AVE y su centro vivo SÓLO en raveV3 (perfil v3). El cliente, raveV2 y Kini no los llevan.
# V26.45: aprobado por el dueño para Almacén RAVE (2026-11-02): el cliente también lleva el equipo y el centro vivo.
if ('p10-centro.js' in parts and (PROFILE=='v3' or V=='cliente') and os.environ.get('R2AVE','1')!='0') or os.environ.get('R2AVE')=='1': parts.append('p10b-r2ave.js');parts.append('p10c-vivo.js') if os.path.exists('p10c-vivo.js') else None
# V26.52 · R2AVE en Telegram (p10d-telegram.js, prompt 4.35): Almacén RAVE (real, con la nube) y raveV3 (demo simulada). Kini y raveV2 no.
if os.path.exists('p10d-telegram.js') and ((V=='cliente' or PROFILE=='v3') and os.environ.get('TG','1')!='0' or os.environ.get('TG')=='1'): parts.append('p10d-telegram.js')
import base64
def kini_brand(h):
    # Marca de la demo Kini: logo y colores (se reemplazan con los del cliente cuando lleguen); los créditos de Vincular Business no se tocan
    lg=os.environ.get('KINI_LOGO','assets/kini-logo.webp')
    if os.path.exists(lg):
        mime='image/png' if lg.endswith('.png') else ('image/webp' if lg.endswith('.webp') else ('image/svg+xml' if lg.endswith('.svg') else 'image/jpeg'))
        uri='data:%s;base64,%s'%(mime,base64.b64encode(open(lg,'rb').read()).decode())
    else:
        svg='<svg xmlns="http://www.w3.org/2000/svg" width="320" height="180" viewBox="0 0 320 180"><rect width="320" height="180" rx="22" fill="#1f3a5f"/><text x="160" y="98" font-family="Arial,Helvetica,sans-serif" font-size="74" font-weight="700" fill="#ffffff" text-anchor="middle">KINI</text><text x="160" y="140" font-family="Arial,Helvetica,sans-serif" font-size="22" letter-spacing="4" fill="#f2b33d" text-anchor="middle">DISTRIBUIDORA</text></svg>'
        uri='data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
    h=re.sub(r'const LOGO_MENU="[^"]*"','const LOGO_MENU="%s"'%uri,h,count=1)
    h=re.sub(r'const LOGO_TICKET="[^"]*"','const LOGO_TICKET="%s"'%uri,h,count=1)
    c1=os.environ.get('KINI_C1','#1b1b1b');c2=os.environ.get('KINI_C2','#5fd33a');c3=os.environ.get('KINI_C3','#3fa521')
    h=h.replace('--ink:#242220;','--ink:%s;'%c1,1).replace('--gold:#c9963e;','--gold:%s;'%c2,1).replace('--gold2:#a87a28;','--gold2:%s;'%c3,1)
    h=h.replace('style="width:48px;height:27px;object-fit:cover;border-radius:6px"','style="width:40px;height:40px;object-fit:contain;border-radius:50%"')
    h=h.replace('Sistema RAVE','Sistema Kini').replace('alt="RAVE"','alt="Kini Distribuidora"')
    h=re.sub(r'<title>[^<]*</title>','<title>Kini Distribuidora · Demo</title>',h,count=1)
    # menú público (documento del iframe): logo, textos fijos y título
    h=re.sub(r'(class=\\"logo\\" src=\\")data:image/[a-z]+;base64,[A-Za-z0-9+/=]+',lambda m:m.group(1)+uri,h,count=1)
    for o,n in [('Almacén y Licorería RAVE, Urquiza 1052, Salta, Argentina. Contacto: WhatsApp 387 4574892.','Kini Distribuidora (demo de evaluación, datos de ejemplo).'),
                ('Almacén y Licorería · Urquiza 1052 · Salta, Argentina','Kini Distribuidora · demo'),
                ('Mirá el menú de Almacén y Licorería RAVE (Urquiza 1052, Salta): vinos, bebidas, cigarrillos y combos. Pedí por WhatsApp 👇','Mirá el catálogo mayorista de Kini Distribuidora. Pedí por WhatsApp 👇'),
                ('Check out the menu of Almacén y Licorería RAVE (Urquiza 1052, Salta): wines, drinks, cigarettes and combos. Order via WhatsApp 👇','Check out the Kini Distribuidora wholesale catalog. Order via WhatsApp 👇'),
                ('Almacén y Licorería RAVE','Kini Distribuidora'),('Almacén y Licorería · Salta','Distribuidora mayorista'),('RAVE DIGITAL','KINI DISTRIBUIDORA'),('Club RAVE','Club Kini'),('class=\\"foot-brand\\">RAVE<','class=\\"foot-brand\\">KINI<'),('alt=\\"RAVE','alt=\\"Kini'),('que RAVE guarde','que Kini Distribuidora guarde'),('RAVE Club','Kini Club'),('<title>RAVE','<title>Kini'),('Este menú incluye bebidas alcohólicas y tabaco.','Este catálogo incluye bebidas alcohólicas.'),('This menu includes alcoholic beverages and tobacco.','This catalog includes alcoholic beverages.')]:
        h=h.replace(o,n)
    h=h.replace('--gold:#c9963e','--gold:%s'%c2)
    h=h.replace('--gold-deep:#dba854','--gold-deep:%s'%c2)

    return h
def solo_brand(h,v3=False):
    # V26.63 · raveV2 = «Mi Negocio»: sistema genérico, sin rubro de negocio (verde comercial).
    #           raveV3 = «Corporación Demo»: visión empresarial, gestión integral (azul corporativo).
    # Nada de Almacén RAVE ni de bebidas/kiosco. Los créditos de Vincular Business no se tocan.
    if v3:
        NM,NMU,TAG,c1,c2,c3,lt='Corporación Demo','CORPORACIÓN DEMO','GESTIÓN INTEGRAL','#0f172a','#3b82f6','#1d4ed8','#60a5fa'
        LOC='Corporación Demo · Casa central · demo'
    else:
        NM,NMU,TAG,c1,c2,c3,lt='Mi Negocio','MI NEGOCIO','DEMO','#1f2a37','#2e8b74','#23695a','#5cc2a8'
        LOC='Mi Negocio · demo'
    fs='27' if v3 else '46'
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="320" height="180" viewBox="0 0 320 180"><rect width="320" height="180" rx="22" fill="%s"/><text x="160" y="92" font-family="Arial,Helvetica,sans-serif" font-size="%s" font-weight="700" fill="#ffffff" text-anchor="middle">%s</text><text x="160" y="136" font-family="Arial,Helvetica,sans-serif" font-size="20" letter-spacing="4" fill="%s" text-anchor="middle">%s</text></svg>'%(c1,fs,NMU,lt,TAG)
    uri='data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
    h=re.sub(r'const LOGO_MENU="[^"]*"','const LOGO_MENU="%s"'%uri,h,count=1)
    h=re.sub(r'const LOGO_TICKET="[^"]*"','const LOGO_TICKET="%s"'%uri,h,count=1)
    h=h.replace('--ink:#242220;','--ink:%s;'%c1,1).replace('--gold:#c9963e;','--gold:%s;'%c2,1).replace('--gold2:#a87a28;','--gold2:%s;'%c3,1)
    h=h.replace('style="width:48px;height:27px;object-fit:cover;border-radius:6px"','style="width:48px;height:27px;object-fit:contain;border-radius:6px"')
    h=h.replace('Sistema RAVE','Sistema VB').replace('alt="RAVE"','alt="%s"'%NM)
    h=re.sub(r'<title>[^<]*</title>','<title>%s · %s · Sistema VB</title>'%(NM,'Gestión empresarial integral' if v3 else 'Sistema de gestión genérico'),h,count=1)
    h=re.sub(r'(class=\\"logo\\" src=\\")data:image/[a-z]+;base64,[A-Za-z0-9+/=]+',lambda m:m.group(1)+uri,h,count=1)
    CAT='nuestro catálogo' if not v3 else 'el catálogo corporativo'
    for o,n in [('Almacén y Licorería RAVE, Urquiza 1052, Salta, Argentina. Contacto: WhatsApp 387 4574892.','%s (demo de evaluación, datos de ejemplo).'%NM),
                ('Almacén y Licorería · Urquiza 1052 · Salta, Argentina',LOC),
                ('Mirá el menú de Almacén y Licorería RAVE (Urquiza 1052, Salta): vinos, bebidas, cigarrillos y combos. Pedí por WhatsApp 👇','Mirá %s de %s. Consultas y pedidos por WhatsApp 👇'%(CAT,NM)),
                ('Check out the menu of Almacén y Licorería RAVE (Urquiza 1052, Salta): wines, drinks, cigarettes and combos. Order via WhatsApp 👇','Check out the %s catalog. Questions and orders via WhatsApp 👇'%NM),
                ('Almacén y Licorería RAVE',NM),('Almacén y Licorería · Salta',LOC),('RAVE DIGITAL',NMU),('Club RAVE','Club '+NM),('class=\\"foot-brand\\">RAVE<','class=\\"foot-brand\\">%s<'%NMU),('alt=\\"RAVE','alt=\\"'+NM),('que RAVE guarde','que %s guarde'%NM),('RAVE Club',NM+' Club'),('<title>RAVE','<title>'+NM),
                ('Este menú incluye bebidas alcohólicas y tabaco.',''),('This menu includes alcoholic beverages and tobacco.','')]:
        h=h.replace(o,n)
    h=h.replace('--gold:#c9963e','--gold:%s'%c2).replace('--gold-deep:#dba854','--gold-deep:%s'%c2)
    # menú lateral: el ítem activo sobre el color de la marca lleva texto negro (contraste ≥ 4,5:1 en verde y en azul)
    h=h.replace('#side a.on{background:var(--gold);color:#1b1100;','#side a.on{background:var(--gold);color:#000;',1)
    # Centro Inteligente: variante más clara del acento para 4,5:1 sobre su fondo oscuro
    h=h.replace('--ci-acc:var(--gold,#c9963e)','--ci-acc:%s'%('#60a5fa' if v3 else '#45ad92'),1)
    h=h.replace('</style>','.btn.gold,.fk.gold,.fk.gold small,.cmp .btn.gold,html[data-theme=dark] .btn.gold,html[data-theme=dark] .fk.gold,html[data-theme=dark] .fk.gold small{color:#000!important}html[data-theme=dark] .cmp-tab.on{color:%s}html[data-theme=dark]{--gold2:%s}\n</style>'%(lt,lt),1)
    return h
import json,os
def gym_brand(h,nc=False):
    # V27.2 · gym = «Mi Gimnasio»: oscuro deportivo con verde lima (referencia visual aprobada por el dueño).
    #         nc  = «Movimiento Inteligente» de Nahuel Cornu: su logo, su nombre y sus colores (nebulosa azul noche, turquesa y rosa, Fraunces + Jost).
    # Nada de Almacén RAVE. Los créditos de Vincular Business no se tocan.
    if nc:
        NM,NMU,c1,c2,c3,lt='Movimiento Inteligente','MOVIMIENTO INTELIGENTE','#060b21','#3de0c5','#1fb5a0','#3de0c5'
        LOC='Entrenamiento personalizado · Nahuel Cornu · Salta'
        uri='data:image/jpeg;base64,'+base64.b64encode(open('assets/nc-logo.jpeg','rb').read()).decode()
        fonts='<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Jost:wght@300;400;500;600;700&display=swap">'
        theme=NC_CSS; tkey='rave.theme.minc'
    else:
        NM,NMU,c1,c2,c3,lt='Mi Gimnasio','MI GIMNASIO','#111111','#c6f135','#9fca12','#c6f135'
        LOC='Mi Gimnasio · demo'
        svg='<svg xmlns="http://www.w3.org/2000/svg" width="320" height="180" viewBox="0 0 320 180"><rect width="320" height="180" rx="22" fill="#151515"/><circle cx="66" cy="90" r="38" fill="none" stroke="#c6f135" stroke-width="14" stroke-dasharray="190 60" transform="rotate(-40 66 90)"/><circle cx="66" cy="90" r="12" fill="#c6f135"/><text x="118" y="86" font-family="Arial,Helvetica,sans-serif" font-size="34" font-weight="800" fill="#ffffff">MI</text><text x="118" y="122" font-family="Arial,Helvetica,sans-serif" font-size="30" font-weight="800" fill="#c6f135">GIMNASIO</text></svg>'
        uri='data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
        fonts='<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap">'
        theme=GYM_THEME; tkey='rave.theme.gym'
    h=re.sub(r'const LOGO_MENU="[^"]*"','const LOGO_MENU="%s"'%uri,h,count=1)
    h=re.sub(r'const LOGO_TICKET="[^"]*"','const LOGO_TICKET="%s"'%uri,h,count=1)
    h=h.replace('--ink:#242220;','--ink:%s;'%c1,1).replace('--gold:#c9963e;','--gold:%s;'%c2,1).replace('--gold2:#a87a28;','--gold2:%s;'%c3,1)
    h=h.replace('style="width:48px;height:27px;object-fit:cover;border-radius:6px"','style="width:40px;height:40px;object-fit:%s;border-radius:10px"'%('cover' if nc else 'contain'))
    h=h.replace('<span>Sistema RAVE</span></a>','<span>%s</span></a>'%NM,1)
    h=h.replace('Sistema RAVE','Sistema VB').replace('alt="RAVE"','alt="%s"'%NM)
    h=re.sub(r'<title>[^<]*</title>','<title>%s · %s</title>'%(NM,'Entrenamiento personalizado · Nahuel Cornu' if nc else 'Sistema VB para gimnasios · demo'),h,count=1)
    h=h.replace('<title>',fonts+'\n<title>',1)
    h=re.sub(r'(class=\\"logo\\" src=\\")data:image/[a-z+]+;base64,[A-Za-z0-9+/=]+',lambda m:m.group(1)+uri,h,count=1)
    for o,n in [('Almacén y Licorería RAVE, Urquiza 1052, Salta, Argentina. Contacto: WhatsApp 387 4574892.','%s%s.'%(NM,' · Nahuel Cornu, Salta' if nc else ' (demo de evaluación, datos de ejemplo)')),
                ('Almacén y Licorería · Urquiza 1052 · Salta, Argentina',LOC),
                ('Mirá el menú de Almacén y Licorería RAVE (Urquiza 1052, Salta): vinos, bebidas, cigarrillos y combos. Pedí por WhatsApp 👇','Mirá los planes de %s. Consultas por WhatsApp 👇'%NM),
                ('Check out the menu of Almacén y Licorería RAVE (Urquiza 1052, Salta): wines, drinks, cigarettes and combos. Order via WhatsApp 👇','Check out the %s plans. Questions via WhatsApp 👇'%NM),
                ('Almacén y Licorería RAVE',NM),('Almacén y Licorería · Salta',LOC),('RAVE DIGITAL',NMU),('Club RAVE','Club '+NM),('class=\\"foot-brand\\">RAVE<','class=\\"foot-brand\\">%s<'%NMU),('alt=\\"RAVE','alt=\\"'+NM),('que RAVE guarde','que %s guarde'%NM),('RAVE Club',NM+' Club'),('<title>RAVE','<title>'+NM),
                ('Este menú incluye bebidas alcohólicas y tabaco.',''),('This menu includes alcoholic beverages and tobacco.','')]:
        h=h.replace(o,n)
    h=h.replace('--gold:#c9963e','--gold:%s'%c2).replace('--gold-deep:#dba854','--gold-deep:%s'%c2)
    h=h.replace('#side a.on{background:var(--gold);color:#1b1100;','#side a.on{background:var(--gold);color:#000;',1)
    h=h.replace('</style>','.btn.gold,.fk.gold,.fk.gold small,.cmp .btn.gold,html[data-theme=dark] .btn.gold,html[data-theme=dark] .fk.gold,html[data-theme=dark] .fk.gold small{color:#000!important}html[data-theme=dark] .cmp-tab.on{color:%s}html[data-theme=dark]{--gold2:%s}\n'%(lt,lt)+GYM_CSS+'\n'+theme+'\n</style>',1)
    # tema del panel: oscuro por defecto y preferencia propia de este sitio (los repositorios comparten el origen raveholding.github.io)
    h=h.replace("function themePref(){try{const v=localStorage.getItem('rave.theme');return THEMES[v]?v:'auto';}","function themePref(){try{const v=localStorage.getItem('%s');return THEMES[v]?v:'dark';}"%tkey,1)
    # V27.4 · el botón de tema alterna Claro / Oscuro y guarda en la misma clave que lee
    h=h.replace("A.themeCycle=()=>{const o=['auto','light','dark'];const n=o[(o.indexOf(themePref())+1)%3];try{localStorage.setItem('rave.theme',n);}","A.themeCycle=()=>{const n=themeEff()==='dark'?'light':'dark';try{localStorage.setItem('%s',n);}"%tkey,1)
    assert "localStorage.setItem('%s',n)"%tkey in h
    # reproductor de YouTube embebido dentro del sistema
    h=h.replace("frame-src https://www.google.com;","frame-src https://www.google.com https://www.youtube-nocookie.com;",1)

    h=h.replace("localStorage.setItem('rave.theme',n)","localStorage.setItem('%s',n)"%tkey,1)
    # vocabulario de gimnasio en la barra
    h=h.replace("club:{t:()=>IS_CLIENT?'Club RAVE':'Club de clientes'","club:{t:()=>'Club de %s'"%('alumnos' if nc else 'socios'),1)
    # menú público con la misma identidad (CSS sin comillas dobles ni barras: va dentro del documento del menú)
    i=h.find('const PUB_DOC="');j=h.find('<\\/style>',i)
    if i>=0 and j>0: h=h[:j]+(NC_PUB if nc else GYM_PUB)+h[j:]
    # V27.3 menú público rediseñado (gimnasio / entrenador)
    i=h.find('const PUB_DOC="')
    if i>=0:
        k=i+len('const PUB_DOC=')
        e=k+1
        while h[e]!='"':
            e+=2 if h[e]=='\\' else 1
        e+=1
        doc=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'capa-gimnasio','p11-pub.html') if os.path.exists('capa-gimnasio/p11-pub.html') else 'p11-pub.html').read()
        V=dict(NAME='Movimiento Inteligente' if nc else 'Gimnasio Demo',KEY='minc' if nc else 'svbgym',NC='true' if nc else 'false',WAFB='5493874484132',
          BG='#060b21' if nc else '#0a0a0a',BG2='#0b1440' if nc else '#121212',CARD='rgba(255,255,255,.06)' if nc else '#121212',
          ACC='#3de0c5' if nc else '#a3e635',ACC2='#6ff0da' if nc else '#ccff00',
          FD="'Fraunces',Georgia,serif" if nc else "'Poppins',system-ui,sans-serif",FU="'Jost',system-ui,sans-serif" if nc else "'Poppins',system-ui,sans-serif",
          BODYBG='radial-gradient(620px 480px at 10% 0%,rgba(61,224,197,.16),transparent 70%),radial-gradient(620px 520px at 95% 30%,rgba(255,106,169,.12),transparent 70%),#060b21' if nc else '#0a0a0a',
          FONTS='<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family='+('Fraunces:wght@600;700;800&family=Jost:wght@400;500;600' if nc else 'Poppins:wght@400;500;600;700;800')+'&display=swap">')
        for a,b in V.items(): doc=doc.replace('__'+a+'__',b)
        h=h[:k]+json.dumps(doc).replace('</','<\\/')+h[e:]
    if nc:
        h=h.replace("'<span class=\"demo-b\">DEMO DE EVALUACIÓN</span>'","''")
        h=h.replace('Demo de evaluación. Usuarios de prueba:','Usuarios iniciales (cambiá los PIN en Usuarios y permisos):')
    return h
GYM_CSS='''.g-idle{border:2px dashed var(--line,#ccc);border-radius:14px;padding:1.2rem;text-align:center;display:flex;flex-direction:column;gap:.3rem}
.g-gate{border-radius:14px;padding:1rem 1.1rem;border:2px solid}.g-gate.ok{background:var(--okbg);border-color:var(--ok);color:var(--ok)}.g-gate.warn{background:var(--warnbg);border-color:#c98a00;color:#8a5a00}.g-gate.bad{background:var(--redbg);border-color:var(--red);color:var(--red)}.g-gate.mute{border-color:var(--line,#ccc)}
html[data-theme=dark] .g-gate.warn{color:#f3c76a}.g-gt{font-weight:800;letter-spacing:.08em;font-size:.85rem}.g-gn{font-weight:700;font-size:1.6rem}.g-gate ul{margin:.4rem 0 0;padding-left:1.1rem}
.g-meter{height:8px;border-radius:99px;background:rgba(127,127,127,.22);overflow:hidden;margin:.3rem 0}.g-meter i{display:block;height:100%;background:var(--gold);border-radius:99px}.g-meter.full i{background:var(--red)}
.g-days{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:.8rem;margin-bottom:1rem}.g-cls{border-top:1px solid rgba(127,127,127,.2);padding:.5rem 0;display:flex;flex-direction:column;gap:.25rem}
.g-bars{display:grid;grid-template-columns:repeat(8,1fr);gap:.4rem;align-items:end;height:130px}.g-bars div{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;font-size:.72rem;gap:.15rem}.g-bars i{display:block;width:70%;background:var(--gold);border-radius:6px 6px 0 0;min-height:2px}
.g-kiosk{position:fixed;inset:0;z-index:9000;background:var(--bg,#fff);overflow:auto;padding:1.2rem}.g-kin{max-width:860px;margin:0 auto;display:flex;flex-direction:column;gap:1rem}.g-clock{font-weight:700;font-size:1.6rem}
.g-home{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:1rem;align-items:start}.g-home>.g-hero{grid-column:1/-1}.g-main{display:flex;flex-direction:column;gap:1rem;min-width:0}.g-side{display:flex;flex-direction:column;gap:.8rem;min-width:0}
@media (max-width:1100px){.g-home{grid-template-columns:1fr}}
.g-hero{position:relative;overflow:hidden;border-radius:22px;min-height:230px;display:flex;align-items:center;background:linear-gradient(110deg,#0d0d0d 0%,#1c1f14 55%,#2b3510 100%);color:#fff;border:1px solid rgba(255,255,255,.06)}
.g-hero .g-art{position:absolute;right:0;top:0;height:100%;width:58%;opacity:.95;-webkit-mask-image:linear-gradient(90deg,transparent,#000 35%);mask-image:linear-gradient(90deg,transparent,#000 35%)}
.g-hero-t{position:relative;z-index:1;padding:1.6rem 2rem;max-width:560px}.g-kick{font-size:.78rem;font-weight:700;letter-spacing:.14em;opacity:.9}.g-hero h2{font-size:clamp(1.7rem,3.2vw,2.6rem);line-height:1.08;margin:.3rem 0 .5rem;font-weight:800;letter-spacing:-.01em;color:#fff}.g-hero h2 b{color:var(--gold)}.g-hero p{margin:0 0 1rem;opacity:.85}
.g-hero .btn:not(.gold){background:rgba(255,255,255,.08);color:#fff;border-color:rgba(255,255,255,.2)}
.g-hero-logo{position:absolute;right:2rem;top:50%;transform:translateY(-50%);height:82%;max-height:200px;border-radius:20px;box-shadow:0 0 60px rgba(61,224,197,.35)}
.g-ico{display:inline-grid;place-items:center;width:36px;height:36px;border-radius:10px;background:rgba(127,127,127,.15);color:var(--gold)}.g-ico svg{width:20px;height:20px}
.g-stat{display:flex;flex-direction:column;gap:.6rem;cursor:pointer}.g-big{font-size:1.9rem;font-weight:800;line-height:1}.g-ring{flex:none;color:inherit}
.g-tiles{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.8rem}.g-tile{position:relative;border:0;padding:0;border-radius:16px;overflow:hidden;cursor:pointer;aspect-ratio:4/3;background:#111;color:inherit}.g-tile .g-art{width:100%;height:100%;display:block}
.g-tag{position:absolute;left:.6rem;right:.6rem;bottom:.6rem;background:var(--gold);color:#000;font-weight:700;border-radius:10px;padding:.5rem;font-size:.92rem;text-align:center}
.g-serv{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.8rem}.g-svc{display:flex;flex-direction:column;gap:.35rem;border:1px solid var(--line);background:rgba(127,127,127,.06);border-radius:16px;padding:.5rem;cursor:pointer;text-align:center;color:inherit;font:inherit}.g-svc .g-art{width:100%;aspect-ratio:16/10;border-radius:12px;display:block}.g-svc b{font-size:.86rem;letter-spacing:.04em;text-transform:uppercase}.g-svc span{font-size:.78rem;color:var(--mut)}
@media (max-width:760px){.g-tiles{grid-template-columns:1fr 1fr}.g-serv{grid-template-columns:1fr 1fr}.g-hero .g-art{width:100%;opacity:.25}.g-hero-logo{opacity:.25}}
.g-mini{display:grid;grid-template-columns:repeat(3,1fr);text-align:center;gap:.4rem}.g-mini div{display:flex;flex-direction:column;gap:.1rem}.g-mini span{font-size:.78rem;color:var(--mut)}.g-acc{color:var(--gold);font-size:1.25rem}
html:not([data-theme=dark]) .g-acc{color:var(--gold2)}
.g-kcal b{display:block;font-size:1.05rem}.g-pb{display:grid;grid-template-columns:120px 1fr;gap:.6rem;align-items:center;font-size:.8rem;margin-top:.35rem}
.g-pair .card{display:flex;flex-direction:column;gap:.3rem}
.g-plan{display:flex;gap:.8rem;align-items:center;text-align:left;width:100%;cursor:pointer;color:inherit;font:inherit}.g-plan .g-art{width:84px;height:64px;border-radius:12px;flex:none}.g-plan b{display:block}.g-plan .g-meter{margin-top:.4rem}
.g-pill{font-size:.72rem;font-weight:700;background:var(--gold);color:#000;border-radius:99px;padding:.2rem .55rem;flex:none}'''
GYM_THEME='''html[data-theme=dark]{--ink:#f4f4f5;--bg:#161616;--card:#222222;--line:#303030;--mut:#a1a1aa;--selbg:#2a3312;--gold:#c6f135;--gold2:#c6f135;--okbg:#18301c;--ok:#7ee28f}
html{--gold:#c6f135}html:not([data-theme=dark]){--gold2:#5b7a00}
#side,html[data-theme=dark] #side{background:#121212!important}
#side a{border-radius:12px}#side a.on,#side a.on:hover{background:var(--gold)!important;color:#000!important}
.ux-pos-btn{box-shadow:0 6px 18px rgba(198,241,53,.22)!important}
html[data-theme=dark] #top{background:#161616!important;border-color:#262626!important}
.card{border-radius:18px}html[data-theme=dark] .card{border-color:#2a2a2a}
h1,h2,h3{font-family:Poppins,system-ui,sans-serif!important;font-weight:700;letter-spacing:-.01em}
html[data-theme=dark] .ux-tabs a.on{color:var(--gold);border-color:var(--gold)}
html[data-theme=dark] .btn.on{background:var(--gold);color:#000;border-color:var(--gold)}'''
NC_CSS='''html[data-theme=dark]{--ink:#eaeefb;--bg:#060b21;--card:rgba(255,255,255,.065);--line:rgba(255,255,255,.13);--mut:#9ea9cc;--selbg:rgba(61,224,197,.14);--gold:#3de0c5;--gold2:#3de0c5;--okbg:rgba(52,211,153,.15);--ok:#34d399;--redbg:rgba(255,93,108,.16);--red:#ff5d6c;--warnbg:rgba(255,184,92,.16)}
html{--gold:#3de0c5}html:not([data-theme=dark]){--gold2:#0a8a78}
html[data-theme=dark] body{background:radial-gradient(520px 420px at 12% 6%,rgba(61,224,197,.20),transparent 70%),radial-gradient(560px 460px at 94% 20%,rgba(86,110,255,.20),transparent 70%),radial-gradient(620px 520px at 60% 100%,rgba(255,106,169,.16),transparent 70%),#060b21 fixed}
body{font-family:Jost,'Segoe UI',system-ui,sans-serif!important}
h1,h2,h3,.g-big,.g-gn{font-family:Fraunces,Georgia,serif!important;font-weight:600;letter-spacing:-.01em}
#side,html[data-theme=dark] #side{background:rgba(4,8,28,.94)!important;border-right:1px solid rgba(255,255,255,.08)}
#side a{border-radius:12px}#side a.on,#side a.on:hover{background:linear-gradient(90deg,#3de0c5,#7ff0dd)!important;color:#04122a!important}
.ux-pos-btn{background:linear-gradient(90deg,#3de0c5,#ff6aa9)!important;color:#04122a!important;box-shadow:0 8px 24px rgba(61,224,197,.25)!important}
html[data-theme=dark] #top{background:rgba(6,11,33,.85)!important;border-color:rgba(255,255,255,.08)!important;backdrop-filter:blur(14px)}
html[data-theme=dark] .card{backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);box-shadow:inset 0 1px 0 rgba(255,255,255,.16),0 12px 40px rgba(0,0,0,.35)!important;border-radius:20px}
html[data-theme=dark] .dlg{background:#0d1533!important;border:1px solid rgba(255,255,255,.12)}
html[data-theme=dark] input,html[data-theme=dark] select,html[data-theme=dark] textarea{background:rgba(4,10,34,.65)!important;border-color:rgba(255,255,255,.16)!important}
html[data-theme=dark] .ux-tabs a.on{color:#3de0c5;border-color:#3de0c5}
html[data-theme=dark] .btn.on{background:#3de0c5;color:#04122a;border-color:#3de0c5}
.g-hero.nc{background:radial-gradient(420px 300px at 85% 40%,rgba(61,224,197,.35),transparent 70%),radial-gradient(380px 300px at 60% 110%,rgba(255,106,169,.30),transparent 70%),linear-gradient(120deg,#060b21,#0b1440)}
.g-hero.nc h2 b{background:linear-gradient(90deg,#3de0c5,#ff6aa9);-webkit-background-clip:text;background-clip:text;color:transparent}
.g-tag,.g-pill{background:linear-gradient(90deg,#3de0c5,#7ff0dd)!important;color:#04122a!important}'''
GYM_PUB=' :root,:root[data-theme],html{--cream:#161616!important;--card-bg:#222222!important;--ink:#f4f4f5!important;--line:#303030!important;--muted:#a1a1aa!important;--charcoal:#0f0f0f!important;--charcoal-2:#0f0f0f!important;--gold:#c6f135!important;--gold-deep:#c6f135!important;color-scheme:dark} body{background:#161616!important;color:#f4f4f5} '
NC_PUB=' :root,:root[data-theme],html{--cream:#060b21!important;--card-bg:rgba(255,255,255,.07)!important;--ink:#eaeefb!important;--line:rgba(255,255,255,.14)!important;--muted:#9ea9cc!important;--charcoal:#0b1440!important;--charcoal-2:#0b1440!important;--gold:#3de0c5!important;--gold-deep:#3de0c5!important;color-scheme:dark} body{background:radial-gradient(520px 420px at 12% 6%,rgba(61,224,197,.22),transparent 70%),radial-gradient(560px 460px at 94% 20%,rgba(86,110,255,.2),transparent 70%),radial-gradient(620px 520px at 60% 100%,rgba(255,106,169,.18),transparent 70%),#060b21 fixed!important;color:#eaeefb} '

vbj='const VB_BANNER="data:image/webp;base64,'+base64.b64encode(open('assets/vb-banner.webp','rb').read()).decode()+'";\n'
html=head+'\n'+vbj+B('build/p0-data.js')+B('build/p0-pub.js')+"const SOCIAL_ICONS_OK=1;\n"+B('build/qr.js')+'\n'+'\n'.join(B(p) for p in parts)+'\n</script>\n</body></html>\n'
if KINI: html=kini_brand(html)
if PROFILE in('solo','v3'): html=solo_brand(html,PROFILE=='v3')
if PROFILE in('gym','nc'): html=gym_brand(html,PROFILE=='nc')
open(out,'w',encoding='utf8').write(html)
m=re.search(r'\n<script>\n(.*?)\n</script>\n</body>',html,re.S)
open('all.js','w',encoding='utf8').write(m.group(1))
subprocess.check_call(['node','--check','all.js'])
print('BUILD OK',V,out,len(html))
