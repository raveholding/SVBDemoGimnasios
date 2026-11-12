#!/usr/bin/env python3
"""Genera portero.html + timbre.html (edición gimnasio / entrenador) a partir del Portero Digital SVB.
Uso (desde fuente/):  python3 capa-gimnasio/gen_portero.py gym|nc ../index.html ../
Integra el portero con el sistema del gimnasio: lee los socios de la base del sistema (mismo sitio),
valida la cuota (al día, en gracia, vencida, congelada), acepta el QR dinámico de la app, el número de socio
o el DNI, y deja cada ingreso en una bandeja que el sistema importa a Control de acceso."""
import sys, os, re, json
prof, idx, out = sys.argv[1], sys.argv[2], sys.argv[3]
NC = prof == 'nc'
here = os.path.dirname(os.path.abspath(__file__))
P = open(os.path.join(here, 'portero_base.html'), encoding='utf-8').read()
T = open(os.path.join(here, 'timbre_base.html'), encoding='utf-8').read()
H = open(idx, encoding='utf-8').read()
logo = re.search(r'const LOGO_MENU="([^"]*)"', H).group(1)
build = json.loads(re.search(r'RAVE_BUILD=(\{[^}]*\})', H).group(1))
DB = build['db']; PUB = build['publicUrl']
KEY = 'mipt_' if NC else 'gpt_'
BRAND = 'Movimiento Inteligente' if NC else 'Mi Gimnasio'
SUB = 'Entrenamiento personalizado · Nahuel Cornu' if NC else 'Gimnasio · Salta'
TAG = 'Entrenamiento a tu medida' if NC else 'Entrená. Superate. Volvé mañana.'
ACC, ACC2, M, M2 = (('#3DE0C5', '#D6FBF4', '#FF6AA9', '#FFE1EE') if NC else ('#C6F135', '#F1FBD0', '#4D7C0F', '#E5F5C8'))
WORD = ('alumno', 'alumnos', 'Alumno') if NC else ('socio', 'socios', 'Socio')

def rep(s, a, b, n=1, need=True):
    if need: assert a in s, a[:80]
    return s.replace(a, b) if n == 0 else s.replace(a, b, n)

s = P
# marca y textos
s = rep(s, '<title>Portero Digital · Cannabismática</title>', '<title>Portero Digital · %s</title>' % BRAND)
s = rep(s, "brand:'Cannabismática', sub:'Asociación civil de cannabis medicinal · Salta', tagline:'Cannabis medicinal con acompañamiento',",
        "brand:%s, sub:%s, tagline:%s," % (json.dumps(BRAND), json.dumps(SUB), json.dumps(TAG)))
s = rep(s, ' * Vincular Business · Portero Digital · Cannabismática', ' * Vincular Business · Portero Digital · edición %s (%s)' % ('entrenador' if NC else 'gimnasio', BRAND))
s = rep(s, "--y:#A8E600; --y2:#EEF9CC; --m:#1F8A70; --m2:#D7F2EA;", "--y:%s; --y2:%s; --m:%s; --m2:%s;" % (ACC, ACC2, M, M2))
s = re.sub(r'const LOGO="[^"]*";', 'const LOGO=%s;' % json.dumps(logo), s, count=1)
s = rep(s, "'WhatsApp de la asociación para que el visitante escriba (opcional)'", "'WhatsApp de recepción para que el visitante escriba (opcional)'")
s = rep(s, "dl('portero_cannabismatica_esp32.ino'", "dl('portero_%s_esp32.ino'" % ('movimiento_inteligente' if NC else 'gimnasio'))
s = rep(s, "S.notif.ntfy.topic='cannabismatica-'", "S.notif.ntfy.topic='%s-'" % ('movimiento' if NC else 'gimnasio'))
s = rep(s, "'https://raveholding.github.io/PorteroCannabismatica/timbre.html'", json.dumps(PUB + 'timbre.html').replace('"', "'"))
# claves propias (el dominio se comparte con otras demos)
s = s.replace("'cnb_", "'" + KEY).replace("'cnb|'", "'%s|'" % KEY[:-1]).replace("s='cnb|'+s", "s='%s|'+s" % KEY[:-1]).replace("S.qr.topic='cnb-'", "S.qr.topic='%s-'" % KEY[:-1])
s = s.replace('window.__cnb=', 'window.__gpt=window.__cnb=')
# pases de visita con prefijo propio
s = s.replace('CNB-', 'PSE-')
# áreas del gimnasio
areas_old = re.search(r"if\(!AREAS\)\{AREAS=\[[\s\S]*?\];\}", s).group(0)
if NC:
    areas = """if(!AREAS){AREAS=[
    {id:uid(),name:'Entrenador',desc:'Nahuel te atiende enseguida',icon:'sofa',wa:'',chime:''},
    {id:uid(),name:'Evaluación inicial',desc:'Primera visita y entrevista',icon:'stethoscope',wa:'',chime:''},
    {id:uid(),name:'Planes y pagos',desc:'Cuotas, planes y consultas',icon:'card',wa:'',chime:''}];}"""
else:
    areas = """if(!AREAS){AREAS=[
    {id:uid(),name:'Recepción',desc:'Información, clase de prueba y altas',icon:'sofa',wa:'',chime:''},
    {id:uid(),name:'Sala de musculación',desc:'Profes de sala y rutinas',icon:'stethoscope',wa:'',chime:''},
    {id:uid(),name:'Clases',desc:'Funcional, spinning, yoga y más',icon:'book',wa:'',chime:''},
    {id:uid(),name:'Entrenador personal',desc:'Turnos y evaluaciones',icon:'doc',wa:'',chime:''},
    {id:uid(),name:'Administración y cuotas',desc:'Pagos, planes y lockers',icon:'card',wa:'',chime:''}];}"""
s = s.replace(areas_old, areas, 1)
s = rep(s, "<small>${en?'Socios y equipo':'Solo personal'}</small>", "<small>${en?'Equipo del %s':'Solo personal'}</small>" % ('entrenador' if NC else 'gimnasio'))
s = rep(s, '<span>Portero Digital SVB · v1.1</span>', '<span>Portero Digital SVB · v1.2 · edición %s</span>' % ('entrenador' if NC else 'gimnasio'))

# tile principal para socios + integración
s = rep(s, """     <button class="tile main" data-act="bell" ${dis}>${ic('bell')}<span><b>Tocar timbre</b><small>Avisá que llegaste y elegí el área</small></span></button>""",
"""     <button class="tile main gx-soc" data-act="gxsoc" ${dis} style="grid-column:1/-1;flex-direction:row;align-items:center;gap:16px;min-height:96px">${ic('ticket')}<span><b>Soy %s · entrar</b><small>Mostrá el QR de tu app en el lector o escribí tu DNI${GX.n?'':' · '+GX.msg}</small></span></button>
     <button class="tile" data-act="bell" ${dis}>${ic('bell')}<span><b>Tocar timbre</b><small>Primera vez, clase de prueba o consultas</small></span></button>""" % WORD[0])
# lector QR tipo teclado: también códigos de socio (SG-00012 / SG-00012.123456)
s = rep(s, "else if(e.key==='Enter'&&/PSE-\\d{6}$/.test(scan.b||'')){",
        "else if(e.key==='Enter'&&/(SG|MI)-\\d{5}(\\.\\d{6})?$/i.test(scan.b||'')&&VIEW!=='admin'){const c=(scan.b.match(/(SG|MI)-\\d{5}(\\.\\d{6})?$/i)||[''])[0];scan.b='';gxCheck('qr',c);}\n  else if(e.key==='Enter'&&/PSE-\\d{6}$/.test(scan.b||'')){")
# teclado en modo socio: DNI o número
s = rep(s, "  if(KP.mode==='pass'){return redeemPass(code)}", "  if(KP.mode==='pass'){return redeemPass(code)}\n  if(KP.mode==='socio'){return gxCheck('dni',code)}")

GX = r"""
/* ====================== integración con el sistema del gimnasio ======================
   Lee los socios de la base del sistema (mismo sitio, sólo lectura) y valida la cuota en la puerta.
   Cada ingreso queda en una bandeja que el sistema importa a Control de acceso.
   No hay datos de socios en este archivo: si el sistema nunca se abrió en este equipo, el portero lo avisa. */
const GXDB=__DB__,GXCODE=__PRE__,GXW=__WORD__,GXOUT='gym-portero-out:'+GXDB;
const GX={n:0,at:0,msg:'abrí el sistema una vez en este equipo para cargar los '+GXW[1],st:null};
function gxLoad(){return new Promise(res=>{try{const r=indexedDB.open(GXDB,1);r.onupgradeneeded=()=>{try{r.result.createObjectStore('kv')}catch(_){}};
  r.onsuccess=()=>{try{const q=r.result.transaction('kv').objectStore('kv').get('state');q.onsuccess=()=>{GX.st=q.result||null;GX.at=now();GX.n=GX.st&&GX.st.gym?Object.keys(GX.st.gym.m||{}).length:0;
    if(GX.st&&GX.st.tenant){if(!LS.get(__K__+'brandset',0)&&GX.st.tenant.name){S.brand=GX.st.tenant.name;}}res(GX.n)};q.onerror=()=>res(0)}catch(e){res(0)}};r.onerror=()=>res(0)}catch(e){res(0)}})}
const gxToday=()=>{const d=new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')};
const gxAdd=(ds,n)=>{const d=new Date(ds+'T12:00:00');d.setDate(d.getDate()+n);return d.toISOString().slice(0,10)};
const gxDmy=ds=>ds?ds.slice(8,10)+'/'+ds.slice(5,7)+'/'+ds.slice(2,4):'';
function gxSha(b){const K=[0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
 let h=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19];const l=b.length,n=((l+9+63)>>6)<<6,m=new Uint8Array(n);m.set(b);m[l]=0x80;const bl=l*8;for(let i=0;i<4;i++)m[n-1-i]=(bl>>>(8*i))&255;
 const w=new Uint32Array(64),r=(x,y)=>(x>>>y)|(x<<(32-y));for(let o=0;o<n;o+=64){for(let i=0;i<16;i++)w[i]=(m[o+4*i]<<24)|(m[o+4*i+1]<<16)|(m[o+4*i+2]<<8)|m[o+4*i+3];
  for(let i=16;i<64;i++){const s0=r(w[i-15],7)^r(w[i-15],18)^(w[i-15]>>>3),s1=r(w[i-2],17)^r(w[i-2],19)^(w[i-2]>>>10);w[i]=(w[i-16]+s0+w[i-7]+s1)|0;}
  let[a,bb,c,d,e,f,g,hh]=h;for(let i=0;i<64;i++){const S1=r(e,6)^r(e,11)^r(e,25),ch=(e&f)^(~e&g),t1=(hh+S1+ch+K[i]+w[i])|0,S0=r(a,2)^r(a,13)^r(a,22),mj=(a&bb)^(a&c)^(bb&c),t2=(S0+mj)|0;hh=g;g=f;f=e;e=(d+t1)|0;d=c;c=bb;bb=a;a=(t1+t2)|0;}
  h=[h[0]+a|0,h[1]+bb|0,h[2]+c|0,h[3]+d|0,h[4]+e|0,h[5]+f|0,h[6]+g|0,h[7]+hh|0];}
 const out=new Uint8Array(32);h.forEach((v,i)=>{out[4*i]=v>>>24;out[4*i+1]=(v>>>16)&255;out[4*i+2]=(v>>>8)&255;out[4*i+3]=v&255;});return out;}
function gxHmac(k,msg){if(k.length>64)k=gxSha(k);const kk=new Uint8Array(64);kk.set(k);const ip=new Uint8Array(64+msg.length),op=new Uint8Array(96);for(let i=0;i<64;i++){ip[i]=kk[i]^0x36;op[i]=kk[i]^0x5c;}ip.set(msg,64);op.set(gxSha(ip),64);return gxSha(op);}
function gxTotp(key,step){const s2=String(key).replace(/-/g,'+').replace(/_/g,'/');const kb=Uint8Array.from(atob(s2+'==='.slice((s2.length+3)%4)),c=>c.charCodeAt(0));const m=new Uint8Array(8);let x=step;for(let i=7;i>=0;i--){m[i]=x&255;x=Math.floor(x/256);}const h=gxHmac(kb,m),o=h[31]&15;return String((((h[o]&127)<<24)|(h[o+1]<<16)|(h[o+2]<<8)|h[o+3])%1e6).padStart(6,'0');}
function gxFind(kind,v){const st=GX.st;if(!st||!st.gym)return{err:'Todavía no hay '+GXW[1]+' cargados en este equipo.'};const C=st.customers||[];const M=st.gym.m||{};
 if(kind==='dni'){const d=String(v).replace(/\D/g,'');if(!d)return{err:'Escribí tu DNI.'};const c=C.find(x=>M[x.id]&&(String(x.dni||'').replace(/\D/g,'')===d||String(x.num)===String(+d)));return c?{c}:{err:'No encontramos ese DNI. Tocá el timbre de Recepción.'}}
 const t=String(v).trim().toUpperCase(),mt=t.match(/^((?:SG|MI)-\d{5})(?:\.(\d{6}))?$/);if(!mt)return{err:'Código no reconocido.'};
 const c=C.find(x=>M[x.id]&&GXCODE+String(x.num||0).padStart(5,'0')===mt[1]);if(!c)return{err:'Código no reconocido.'};const m=M[c.id];
 const strict=!!(st.gym.pro&&st.gym.pro.cfg&&st.gym.pro.cfg.qrStrict);
 if(mt[2]){if(!m.qk)return{err:'Pedí en recepción que actualicen tu app.'};const k=Math.floor(Date.now()/3e4);if(![k,k-1,k+1].some(z=>gxTotp(m.qk,z)===mt[2]))return{c,err:'Ese QR ya venció: abrí la app para ver el código actual.',deny:'QR vencido o copiado'};return{c,din:true}}
 if(strict)return{c,err:'Mostrá el QR que cambia, desde la app.',deny:'QR fijo no permitido'};return{c};}
function gxState(c){const st=GX.st,m=st.gym.m[c.id],t=gxToday(),g=+(st.gym.cfg&&st.gym.cfg.grace)||0;const pl=(st.gym.plans||[]).find(p=>p.id===m.plan);
 if(c.status==='baja'||m.baja)return{k:'bad',t:'Dado de baja',why:'Consultá en recepción.'};
 if(m.freeze&&m.freeze.from<=t&&m.freeze.until>=t)return{k:'bad',t:'Plan congelado',why:'Tu plan está pausado hasta el '+gxDmy(m.freeze.until)+'.'};
 if(m.due>=t)return{k:'ok',t:'Cuota al día',why:(pl?pl.name+' · ':'')+'vence el '+gxDmy(m.due)};
 if(m.due>=gxAdd(t,-g))return{k:'warn',t:'Cuota vencida · en período de gracia',why:'Venció el '+gxDmy(m.due)+'. Renovala hoy en recepción o desde la app.'};
 return{k:'bad',t:'Cuota vencida',why:'Venció el '+gxDmy(m.due)+'. Renovala en recepción o desde la app.'};}
function gxOut(ev){try{const L=JSON.parse(localStorage.getItem(GXOUT)||'[]');L.push(ev);localStorage.setItem(GXOUT,JSON.stringify(L.slice(-300)))}catch(_){}}
async function gxCheck(kind,v){if(!isEnabled()){audit('OFFHOURS_DENIED',GXW[2]+' fuera de horario');sfx.bad();toast('Portero fuera de servicio · '+hoursTxt(),3500);return}
 if(!GX.st||now()-GX.at>30000)await gxLoad();const r=gxFind(kind,v);const via=kind==='dni'?'DNI':(r.din?'QR dinámico':'QR');
 if(!r.c){audit('MEMBER_UNKNOWN',via+' · '+String(v).slice(0,14));return kind==='dni'&&VIEW==='keypad'?failOne(r.err,'MEMBER_UNKNOWN'):(sfx.bad(),gxShow('bad','No te encontramos',r.err,null))}
 const c=r.c,nm=(c.name||'')+(c.last?' '+c.last:'');
 if(r.err){audit('ACCESS_DENIED',via+' · '+nm+' · '+(r.deny||r.err),nm,false);gxOut({cust:c.id,ts:now(),method:kind==='dni'?'dni':'qr',res:'denied',why:r.deny||r.err,src:'portero'});sfx.bad();return gxShow('bad','No pudimos validar tu QR',r.err,c)}
 const s2=gxState(c);if(s2.k==='bad'){audit('ACCESS_DENIED',via+' · '+nm+' · '+s2.t,nm);gxOut({cust:c.id,ts:now(),method:kind==='dni'?'dni':'qr',res:'denied',why:s2.t,src:'portero'});sfx.bad();say('Hola '+(c.name||'')+'. '+s2.t+'. Consultá en recepción.');return gxShow('bad',s2.t,s2.why,c)}
 FAIL={n:0,until:0};LS.set(__K__+'fail',FAIL);gxOut({cust:c.id,ts:now(),method:kind==='dni'?'dni':'qr',res:s2.k==='warn'?'warn':'ok',why:s2.k==='warn'?s2.t:'',src:'portero'});
 if(s2.k==='warn')toast(s2.t+' · '+s2.why,5000);openDoor(c.name||nm,GXW[2]+' · '+via);}
function gxShow(k,t,why,c){ov(`<div class="box"><div style="font-size:54px;line-height:1">${k==='bad'?'⛔':'⚠️'}</div><h2>${esc(t)}</h2><p>${c?'<b>'+esc(c.name||'')+'</b><br>':''}${esc(why)}</p><div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:12px"><button class="btn y" data-act="gxbellAdm">Llamar a ${esc(gxAdmArea().name)}</button><button class="btn" data-act="gxclose">Cerrar</button></div></div>`);say(t);clearTimeout(gxShow.t);gxShow.t=setTimeout(()=>{if(VIEW!=='admin'){ov(null);go('home')}},12000)}
function gxAdmArea(){return AREAS.find(a=>/admin|cuota|pago|plan/i.test(a.name))||AREAS[0]}
setInterval(()=>{gxLoad().then(()=>{if(VIEW==='home')try{build()}catch(_){}})},60000);
"""
GX = GX.replace('__DB__', json.dumps(DB)).replace('__PRE__', json.dumps('MI-' if NC else 'SG-')).replace('__WORD__', json.dumps(list(WORD))).replace('__K__', json.dumps(KEY))
s = rep(s, "/* ====================== PIN / pases ====================== */", GX + "\n/* ====================== PIN / pases ====================== */")
# acciones nuevas
s = rep(s, "const A={", """const A={
 gxsoc(){startKeypad({mode:'socio',guard:true,title:'Ingresá tu DNI',sub:'O mostrá el QR de tu app en el lector',max:8,min:6,auto:false})},
 gxclose(){ov(null);go('home')},
 gxbellAdm(){ov(null);ringArea(gxAdmArea().id)},""")
# el nombre que pone el dueño en el panel manda sobre el del sistema
s = s.replace("fr.onload=()=>{S.logo=fr.result;", "fr.onload=()=>{S.logo=fr.result;LS.set(%s+'brandset',1);" % json.dumps(KEY))
s = rep(s, "  await ensureDefaults();", "  await ensureDefaults();\n  try{await gxLoad()}catch(_){}")
open(os.path.join(out, 'portero.html'), 'w', encoding='utf-8').write(s)

t = T.replace("|| 'la asociación'", "|| %s" % json.dumps(BRAND).replace('"', "'"))
t = re.sub(r'#A8E600', ACC, t, flags=re.I); t = re.sub(r'#1F8A70', M, t, flags=re.I)
t = t.replace('Cannabismática', BRAND).replace("'cnb_", "'" + KEY)
open(os.path.join(out, 'timbre.html'), 'w', encoding='utf-8').write(t)
print('portero ok', len(s), 'timbre ok', len(t))
