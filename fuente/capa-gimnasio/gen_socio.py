#!/usr/bin/env python3
"""Genera socio.html (app del socio/alumno) para un perfil: gym | nc.  Uso: gen_socio.py <perfil> <base socio.html> <fuente> <salida>"""
import sys,re,base64
prof,base,src,out=sys.argv[1:5]
s=open(base,encoding='utf8').read()
qr=open(src+'/build/qr.js',encoding='utf8').read()
NC=prof=='nc'
if NC:
    logo='data:image/jpeg;base64,'+base64.b64encode(open(src+'/assets/nc-logo.jpeg','rb').read()).decode()
    NM,acc,pre,title='Movimiento Inteligente','#3de0c5','minc','App del alumno · Movimiento Inteligente'
else:
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200"><rect width="200" height="200" rx="40" fill="#151515"/><circle cx="100" cy="86" r="46" fill="none" stroke="#c6f135" stroke-width="18" stroke-dasharray="230 60" transform="rotate(-40 100 86)"/><circle cx="100" cy="86" r="14" fill="#c6f135"/><text x="100" y="172" font-family="Arial,Helvetica,sans-serif" font-size="24" font-weight="800" fill="#ffffff" text-anchor="middle">MI GIMNASIO</text></svg>'
    logo='data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()
    NM,acc,pre,title='Mi Gimnasio','#c6f135','svbgym','App del socio · Mi Gimnasio · Sistema VB'
s=re.sub(r"const LOGO='data:image/[^']+'","const LOGO='%s'"%logo,s,count=1)
s=s.replace('<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>','<script>\n'+qr+'\n</script>')
s=s.replace("if(ui.tab==='inicio'){const el=$('#qr');if(el&&window.QRCode){el.innerHTML='';try{new QRCode(el,{text:D.c,width:216,height:216,colorDark:'#04122a',colorLight:'#ffffff'})}catch(e){el.textContent=D.c}}}",
            "if(ui.tab==='inicio'){const el=$('#qr');if(el&&window.QR){try{el.innerHTML=QR.svg(D.c,5,1);const g=el.querySelector('svg');if(g){g.setAttribute('width','216');g.setAttribute('height','216');}}catch(e){el.textContent=D.c}}}")
assert 'QR.svg(D.c' in s and 'cdnjs' not in s
s=re.sub(r'<title>[^<]*</title>','<title>%s</title>'%title,s,count=1)
# claves propias de este sitio (todos los repositorios comparten el origen raveholding.github.io)
for k in ["'mi-socio'","'mi-done-'","'mi-log'","'mi-theme'"]:
    s=s.replace(k,k.replace('mi-',pre+'-'))
s=s.replace("if(D.ac)document.documentElement.style.setProperty('--teal',D.ac);","document.documentElement.style.setProperty('--teal',D.ac||'%s');"%acc)
# demo con los datos de este perfil
s=s.replace("b:'Movimiento Inteligente',o:'Nahuel Cornu',ac:'',w:'5493874484132',n:'Lucía Ferreyra',c:'MI-DEMO01',p:'Pase libre',pr:38000",
            ("b:'Movimiento Inteligente',o:'Nahuel Cornu',ac:'',w:'',n:'Lucía (ejemplo)',c:'MI-00001',p:'2 sesiones semanales',pr:40000" if NC else "b:'Mi Gimnasio',o:'demo',ac:'',w:'',n:'Lucía (ejemplo)',c:'SG-00001',p:'Pase libre',pr:38000"))
s=s.replace("se:'Sede Centro'","se:''",1)
s=s.replace("pay:['https://link.mercadopago.com.ar/movimientointeligente','movimiento.inteligente']","pay:['','%s']"%('' if NC else 'mi.gimnasio.demo'))
if NC:
    s=re.sub(r"cl:\[\['Spinning',1,'08:00'\][^\n]*?\]\],\n","cl:[['Sesión presencial',2,'18:00'],['Sesión presencial',5,'18:00']],\n",s,count=1)
    s=s.replace("'Batido de proteína gratis',10],['Una clase de personal de regalo',20]","'Una sesión extra de regalo',10]")
    s=s.replace("Vista de demostración de la app del socio. Cada socio recibe la suya por WhatsApp desde el sistema del gimnasio.","Vista de ejemplo de la app del alumno. Cada alumno recibe la suya por WhatsApp desde el sistema.")
    s=s.replace("'Clases'],['avisos'","'Agenda'],['avisos'")
s=re.sub(r"av:\[\[addDays\(t,-2\)[^\n]*\]\],at:t\};","av:[],at:t};",s,count=1)
# créditos completos de Vincular Business (regla 8)
s=s.replace("<b>'+DEV.name+'</b></div></div>","<b>'+DEV.name+'</b><div class=\"meta\" style=\"font-size:13px\"><i>“Tu idea, en buenas manos.”</i> · <a href=\"https://www.vincularbusiness.com.ar/\" target=\"_blank\" rel=\"noopener\" style=\"color:inherit\">vincularbusiness.com.ar</a> · '+DEV.mail+'</div></div></div>")
s=s.replace("'WhatsApp '+DEV.waTxt+'</a>","'Celular '+DEV.waTxt+'</a>")
s=s.replace("WhatsApp '+DEV.waTxt+'</a>","Celular '+DEV.waTxt+'</a>")
s=s.replace("Pagá desde acá y tu membresía se renueva sola cuando se acredita.","Pagá con el link o transferí al alias y avisá que pagaste: la cuota se renueva cuando se confirma el pago.")
if NC:
    for o,n in [("APP DEL SOCIO","APP DEL ALUMNO"),("Pedí en recepción que te midan para seguir tu evolución","Pedile a tu entrenador que te mida para seguir tu evolución"),("Tu membresía no incluye clases grupales.","Todavía no tenés horarios fijos: coordinalos con tu entrenador."),
                 ("el gimnasio confirma el cupo por WhatsApp","tu entrenador confirma el horario por WhatsApp"),("Avisos del gimnasio","Avisos de tu entrenador"),("el gimnasio","tu entrenador")]:
        s=s.replace(o,n)
open(out,'w',encoding='utf8').write(s)
m=re.search(r'<script>\n\(function\(\)\{(.*?)\n\}\)\(\);\n</script>',s,re.S)
open('/tmp/socio_check.js','w').write('(function(){'+m.group(1)+'\n})();')
print('socio ok',out,len(s))
