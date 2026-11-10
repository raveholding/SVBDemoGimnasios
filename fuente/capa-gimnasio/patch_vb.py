#!/usr/bin/env python3
"""Aplica la capa de gimnasio / entrenador personal a una copia de AlmacenRAVE/fuente.
Uso: python3 patch_vb.py <dir fuente>   (idempotente: si ya está aplicado, no cambia nada)"""
import sys,os,shutil
D=sys.argv[1]
def rd(f):return open(os.path.join(D,f),encoding='utf8').read()
def wr(f,s):open(os.path.join(D,f),'w',encoding='utf8').write(s)
def rep(f,old,new,marker):
    s=rd(f)
    if marker in s:return
    assert s.count(old)==1,(f,old[:80],s.count(old))
    wr(f,s.replace(old,new))
here=os.path.dirname(os.path.abspath(__file__))
shutil.copy(os.path.join(here,'p11-gym.js'),os.path.join(D,'p11-gym.js'))
shutil.copy(os.path.join(here,'nc-logo.jpeg'),os.path.join(D,'assets','nc-logo.jpeg'))
rep('p2-core.js',"if(typeof isSoloBuild==='function'&&isSoloBuild())soloBase(r);",
    "if(typeof isSoloBuild==='function'&&isSoloBuild())soloBase(r);if(typeof window!=='undefined'&&window.__gymReady&&isGymBuild())gymBase(r);",'gymBase(r)')
rep('p3o-solo.js',"function isSoloBuild(){return!!(typeof window!=='undefined'&&window.RAVE_BUILD&&(window.RAVE_BUILD.profile==='solo'||window.RAVE_BUILD.profile==='v3'));}",
    "function isSoloBuild(){return!!(typeof window!=='undefined'&&window.RAVE_BUILD&&['solo','v3','gym','nc'].includes(window.RAVE_BUILD.profile));} /* V27.1: gimnasio (gym) y entrenador personal (nc) usan la base de un solo dueño */",'gym\',\'nc\']')
rep('p3o-solo.js'," S.sales=S.sales.filter(s=>s.wch!=='mayorista');}"," S.sales=S.sales.filter(s=>s.wch!=='mayorista');if(typeof gymExtras==='function')gymExtras();}",'gymExtras()')
rep('p4f-rrhh.js',"const deps=V3?['Comercial','Finanzas','Operaciones','Soporte técnico','Recursos Humanos']:['Ventas','Depósito','Administración'];",
    "const deps=V3?['Comercial','Finanzas','Operaciones','Soporte técnico','Recursos Humanos']:(typeof isGymBuild==='function'&&isGymBuild())?['Recepción','Entrenamiento','Mantenimiento']:['Ventas','Depósito','Administración'];",'Entrenamiento\',\'Mantenimiento')
rep('pub/pre.js',"st.textContent='#age-gate,#alc-notice{display:none!important}'","st.textContent='#age-gate,#alc-notice,#alc-legend{display:none!important}'",'#alc-legend{display')
b=rd('build.py')
if "'gym'" not in b:
    b=b.replace("assert V in('demo','cliente','kini','solo','v3')","assert V in('demo','cliente','kini','solo','v3','gym','nc')",1)
    b=b.replace("PROFILE=V if V in('kini','solo','v3') else ''","PROFILE=V if V in('kini','solo','v3','gym','nc') else ''",1)
    b=b.replace("if PROFILE=='v3': pub=os.environ.get('PUBLIC_URL','https://raveholding.github.io/raveV3/')",
      "if PROFILE=='v3': pub=os.environ.get('PUBLIC_URL','https://raveholding.github.io/raveV3/')\n"
      "# V27.1 · gym = demo genérica de gimnasios (SVBDemoGimnasios) · nc = entrenador personal Nahuel Cornu (MovimientoInteligenteNC)\n"
      "if PROFILE=='gym': pub=os.environ.get('PUBLIC_URL','https://raveholding.github.io/SVBDemoGimnasios/')\n"
      "if PROFILE=='nc': pub=os.environ.get('PUBLIC_URL','https://raveholding.github.io/MovimientoInteligenteNC/')",1)
    b=b.replace("'solo':'rave-solo-demo-v1','v3':'rave-v3-demo-v2'}","'solo':'rave-solo-demo-v1','v3':'rave-v3-demo-v2','gym':'rave-gym-demo-v1','nc':'rave-nc-mi-v1'}",1)
    b=b.replace("parts=[p for p in parts if os.path.exists(p)]","parts=[p for p in parts if os.path.exists(p)]\nif PROFILE in('gym','nc'): parts.insert(parts.index('p5c-menusec.js'),'p11-gym.js')",1)
    b=b.replace("PROFILE not in('kini','solo')","PROFILE not in('kini','solo','gym','nc')",1)
    b=b.replace("vbj='const VB_BANNER=",open(os.path.join(here,'gym_brand.py'),encoding='utf8').read()+"\nvbj='const VB_BANNER=",1)
    b=b.replace("if PROFILE in('solo','v3'): html=solo_brand(html,PROFILE=='v3')","if PROFILE in('solo','v3'): html=solo_brand(html,PROFILE=='v3')\nif PROFILE in('gym','nc'): html=gym_brand(html,PROFILE=='nc')",1)
    for k in ["'gym','nc')","rave-gym-demo-v1","p11-gym.js","def gym_brand","html=gym_brand"]:assert k in b,k
    wr('build.py',b)
print('patch ok',D)
