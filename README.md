# Sistema VB para gimnasios · demo

Demo de **Sistema Vincular Business** para gimnasios: el sistema completo de raveV2 (Vender POS, gestión de caja, inventario, Club, Atención al cliente, Recursos Humanos, facturación ARCA, menú público) más el módulo **Gimnasio**. Datos de ejemplo, negocio genérico «Mi Gimnasio».

- Menú público: `/` · Acceso del equipo: `/#acceso`
- Usuarios de prueba: ADMIN 1234 · Supervisor 1111 · Mostrador 0000 · Entrenador 2468
- App del socio: `/socio.html` (sin enlace muestra un ejemplo; cada socio recibe la suya por WhatsApp desde su ficha)

## Módulo Gimnasio (una entrada en la barra, con pestañas)

- **Acceso:** QR de la app, tarjeta NFC (lector USB) o documento. Verde, amarillo o rojo según la cuota, el período de gracia, la membresía congelada, las sesiones de la semana, la declaración de salud, el saldo en cuenta corriente y el aforo. Personas adentro, salida y modo tótem.
- **Socios:** son clientes del Club. Tablero (activos, mora, a cobrar en 7 días, riesgo de abandono), filtros, ficha con resumen, progreso (mediciones y gráficos), rutina e historial. Congelar y descongelar, corregir vencimiento con motivo, avisos por WhatsApp asistido.
- **Membresías:** cada una es un artículo de Inventario. Se cobra en **Vender** (caja, comprobante, ARCA y reportes de siempre) y al cobrarse extiende el vencimiento sola. Reglas de gracia, aviso y aforo; link de pago fijo y alias.
- **Clases:** grilla semanal con cupos, reservas y asistencia.
- **Rutinas:** entrenador inteligente por reglas (objetivo, nivel, lesiones, máquinas operativas, mediciones), edición de cargas, envío por WhatsApp y catálogo de ejercicios con videos.
- **Máquinas:** estado, mantenimiento preventivo con alertas, historial y QR para pegar en cada máquina.
- El **Resumen** suma el tablero del gimnasio y la barra muestra avisos de cuotas vencidas y máquinas para revisar.

## Límites (honestos)

- La huella queda pendiente de dispositivo y revisión legal (dato biométrico): no se simula.
- El link de pago es fijo: la confirmación automática por webhook de Mercado Pago necesita la cuenta del comercio y un servidor. Hoy el pago se confirma cobrando la cuota en Vender.
- La app del socio muestra los datos del último enlace enviado; sin servidor no se sincroniza sola.
- WhatsApp es asistido: cada mensaje lo envía una persona.

## Código

`fuente/` es una copia de la fuente única de Sistema VB (`AlmacenRAVE/fuente`, V26.65) con el módulo `p11-gym.js` y los perfiles `gym` y `nc` en `build.py`. Compilar: `cd fuente && python3 build.py gym ../index.html`. Detalle en `fuente/PROMPT_DEMO_GIMNASIOS.md`.

Desarrollado por **Vincular Business** · Celular (387) 4484132 · https://www.vincularbusiness.com.ar/ · vincularbusiness@gmail.com · *“Tu idea, en buenas manos.”*
