# SISTEMA VB · PERFILES `gym` y `nc` (gimnasio y entrenador personal)

**Versión:** V27.1 · 2026-11-10 · base: `AlmacenRAVE/fuente` V26.65 (misma base que raveV2, perfil `solo`).

| Perfil | Repositorio | Para quién | Base local del navegador |
|---|---|---|---|
| `gym` | `SVBDemoGimnasios` | Demo genérica para gimnasios («Mi Gimnasio», naranja `#f97316`) | `rave-gym-demo-v1` |
| `nc` | `MovimientoInteligenteNC` | Sistema de Nahuel Cornu (Movimiento Inteligente, logo propio, turquesa `#3de0c5`) | `rave-nc-mi-v1` |

Por decisión del dueño (2026-11-10) cada repositorio lleva **su propia copia** de `fuente/`. Las mejoras de Sistema VB se traen copiando la fuente nueva y aplicando de nuevo la capa (ver «Cómo actualizar»).

## Qué agrega la capa

- `p11-gym.js` (módulo nuevo, sólo en `gym` y `nc`): pantallas `gacceso`, `gsocios`, `gplanes`, `gclases` (gym), `gagenda` (nc), `grutinas`, `gmaq`, agrupadas en una entrada con pestañas (`UX_GROUPS.gym`) y sección propia («Gimnasio» / «Entrenamiento»).
- Datos en `S.gym`: `cfg` (gracia, aviso, aforo, link de pago, alias, dirección de la app), `plans` (cada uno apunta a un artículo con `gymPlan`), `m` (membresía por cliente: plan, vencimiento, congelamiento, objetivo, nivel, lesiones, salud, mediciones), `classes`, `res`, `catt`, `att`, `acc`, `slots`, `routines`, `mq`, `ex`, `pays`.
- **Cobro:** se envuelve `commitSale`: si la venta lleva un artículo de membresía exige cliente y, al confirmarse, extiende el vencimiento (desde el vencimiento si está dentro del período de gracia, si no desde hoy) y audita `GYM_CUOTA`.
- Permisos nuevos `gym`, `gym_admin`, `gym_train`; rol `entrenador` (usuario «Entrenador», PIN 2468).
- Resumen con el tablero del gimnasio; avisos en la barra (cuotas vencidas, máquinas para revisar).
- `socio.html`: app del socio/alumno (QR de acceso con `QR.svg` del sistema, cuota, pago, rutina con temporizador, progreso, clases o agenda). Los datos viajan en el enlace (`#s=`) y se guardan en el celular con claves propias del sitio.
- Corrección en `pub/pre.js`: con la venta restringida apagada también se oculta la leyenda de edad del menú (en raveV2 sigue visible).

## Reglas respetadas

Huella pendiente de dispositivo y revisión legal (no se simula). Sin cobros simulados: «Probar sin lector» simula una lectura de QR con datos de ejemplo y está rotulado «demostración». WhatsApp asistido. Créditos de Vincular Business intactos. `nc` no muestra «DEMO DE EVALUACIÓN».

## Cómo actualizar desde la fuente de Sistema VB

La capa está guardada en `capa-gimnasio/` (módulo, logo, parche y generador de la app del socio). Con una fuente nueva:

```
cp -a AlmacenRAVE/fuente/. fuente/            # fuente nueva
python3 fuente/capa-gimnasio/patch_vb.py fuente  # vuelve a aplicar la capa (idempotente)
cd fuente && python3 build.py gym ../index.html  # o: nc
python3 capa-gimnasio/gen_socio.py gym capa-gimnasio/socio_base.html . ../socio.html
```

Después, probar en el navegador (acceso, cobro en Vender, ficha, rutinas, menú público) antes de publicar.

## Pendiente

Nube Supabase para `nc` (falta URL y clave publicable); confirmación automática de pagos por webhook; lector biométrico.
