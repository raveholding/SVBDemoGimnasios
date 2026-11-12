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
    # V27.6 · el dominio raveholding.github.io es compartido por todas las demos y su localStorage puede llenarse
    # con datos de otras: si una preferencia chica no entra, se guarda en una cookie de ESTE sitio (ruta propia).
    LSFIX="""<script>(function(){try{var P=Storage.prototype,si=P.setItem,gi=P.getItem,ri=P.removeItem;if(P.__vbfix)return;P.__vbfix=1;
var path=(location.pathname.replace(/[^/]*$/,'')||'/'),ck=function(k){return 'vbls_'+encodeURIComponent(k).replace(/%/g,'_');},
rd=function(k){var n=ck(k)+'=',a=document.cookie.split('; ');for(var i=0;i<a.length;i++)if(a[i].indexOf(n)===0){try{return decodeURIComponent(a[i].slice(n.length));}catch(e){return null;}}return null;},
wr=function(k,v){document.cookie=ck(k)+'='+encodeURIComponent(v)+';path='+path+';max-age=31536000;SameSite=Lax';};
P.setItem=function(k,v){try{si.call(this,k,v);if(this===window.localStorage&&rd(k)!==null)document.cookie=ck(k)+'=;path='+path+';max-age=0';}catch(e){if(this===window.localStorage&&String(v).length<=1500&&location.protocol!=='file:'){try{ri.call(this,k);}catch(x){}wr(k,String(v));return;}throw e;}};
P.getItem=function(k){if(this===window.localStorage){var c=rd(k);if(c!==null)return c;}return gi.call(this,k);};
P.removeItem=function(k){ri.call(this,k);if(this===window.localStorage&&rd(k)!==null)document.cookie=ck(k)+'=;path='+path+';max-age=0';};}catch(e){}})();</script>"""
    _i=h.find('<script')
    if _i>=0 and 'P.__vbfix' not in h: h=h[:_i]+LSFIX+h[_i:]
    # tema: claro/oscuro propio de este sitio (origen compartido), arranca en oscuro
    h=h.replace("localStorage.getItem('rave.theme')","localStorage.getItem('%s')"%tkey).replace("localStorage.setItem('rave.theme',","localStorage.setItem('%s',"%tkey)
    h=h.replace("return THEMES[v]?v:'auto';}","return THEMES[v]?v:'dark';}",1)
    if "A.themeSet=" in h:
        h=h.replace("A.themeCycle=()=>{const o=['light','dark','auto'];","A.themeCycle=()=>{const o=['light','dark'];",1)
        h=h.replace("A.themeSet({dataset:{t:o[(o.indexOf(themePref())+1)%3]}});};","A.themeSet({dataset:{t:themeEff()==='dark'?'light':'dark'}});};",1)
    else:
        h=h.replace("A.themeCycle=()=>{const o=['auto','light','dark'];const n=o[(o.indexOf(themePref())+1)%3];","A.themeCycle=()=>{const n=themeEff()==='dark'?'light':'dark';",1)
    assert "localStorage.setItem('%s',"%tkey in h
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
GYM_CSS='''.th-seg [data-t=auto]{display:none!important}.g-idle{border:2px dashed var(--line,#ccc);border-radius:14px;padding:1.2rem;text-align:center;display:flex;flex-direction:column;gap:.3rem}
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
