import json
s=open('/tmp/gymsrc/p11-gym.js').read()
mk="/* ======================================================================\n   V28"
k0=s.find(mk);end=s.find("if(typeof window!=='undefined')window.__gymReady=1;")
if k0>=0:s=s[:k0]+s[end:]
k=s.find("if(typeof window!=='undefined')window.__gymReady=1;")
rx=open('/tmp/gymsrc/rx-render.js').read()
add=open('/tmp/gymsrc/p11b-pro.js').read()+'\n'+"/* ======================================================================\n   V29 · renderizador de rutinas */\nconst RX_SRC="+json.dumps(rx).replace('</','<\\/')+";\n"+rx+'\n'+open('/tmp/gymsrc/p11c-rx.js').read()+'\n'
add=add.replace("/* ======================================================================\n   V28","/* ======================================================================\n   V28",1)
s=s[:k]+add+s[k:]
open('/tmp/gymsrc/p11-gym.js','w').write(s);print(len(s))
