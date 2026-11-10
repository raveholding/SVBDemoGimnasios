# Movimiento Inteligente · Sistema para gimnasios

Demo de un sistema de gestión completo para gimnasios, de una o varias sedes. Son tres páginas que se abren directo en el navegador, sin instalar nada:

- `index.html`: el sistema del gimnasio (recepción, administración, profesores).
- `socio.html`: la app del socio, que cada socio recibe por WhatsApp.
- `menu.html`: el menú público para quienes todavía no son socios.

Los datos quedan en el navegador (localStorage).

## Qué incluye el sistema

- **Acceso:** QR de la app, NFC, huella o documento. Resultado verde, amarillo o rojo; abre la cerradura o el molinete solo si corresponde. Estados al día, por vencer, **período de gracia** configurable, vencida, congelada y de otra sede. El personal ficha con el mismo lector. Pulsador de salida, **aforo en vivo** ("adentro ahora") y modo tótem.
- **Socios:** ficha con pestañas (resumen, progreso, rutina, historial), **congelamiento** por vacaciones o lesión que corre el vencimiento solo, importación desde planilla, filtros por gracia, congelados, riesgo de abandono y sin rutina.
- **Membresías:** precios, sesiones por semana y acceso a una o a todas las sedes.
- **Clases:** grilla semanal editable por sede, cupos, reservas y asistencia; entrenamiento personal.
- **Rutinas con entrenador inteligente:** arma la rutina según el objetivo, el nivel, las lesiones, las máquinas que funcionan en la sede del socio y la evolución de sus mediciones. El profesor la revisa, ajusta cargas y la asigna. Catálogo de 36 ejercicios con videos de técnica.
- **Progreso:** mediciones corporales (peso, grasa, cintura, cadera, pecho, brazo, pierna) con gráficos, racha de semanas y asistencias.
- **Máquinas y mantenimiento:** estado, foto, video de uso, QR para pegar en cada máquina, mantenimiento preventivo con alertas y costos que se cargan como gasto. Las máquinas en reparación quedan fuera de las rutinas nuevas.
- **Cobros:** pagos mixtos, link de pago de **Mercado Pago** con renovación automática al acreditarse (simulada en la demo), alias, anulación con motivo, comprobantes internos y libro de ventas para ARCA.
- **Club y avisos:** sellos y premios, campañas de WhatsApp (vencimientos, gracia, cumpleaños, reseñas, riesgo de abandono) y **avisos segmentados** por sede, membresía o clase que también aparecen en la app.
- **Buffet:** punto de venta, stock, vencimientos y cuenta corriente.
- **Personal:** fichaje con PIN o NFC, turnos, horas y liquidación estimada.
- **Administración:** caja, gastos, resultado del mes, ingresos por día, **auditoría** de quién hizo qué, exportación a CSV y resumen diario al WhatsApp del dueño.
- **Multisede, marca y roles:** sedes con su propio acceso, aforo, clases y máquinas; color y logo propios; roles de administrador, supervisor, recepción y entrenador.

## App del socio (`socio.html`)

QR de acceso, estado de la cuota, pago con Mercado Pago o alias, rutina con videos y temporizador de descanso, progreso con gráficos, clases con reserva por WhatsApp, avisos y Club. Se instala en la pantalla de inicio.

Desde la ficha del socio: **Enviar la app por WhatsApp**. El enlace lleva los datos del socio y se guarda en su celular; se actualiza cada vez que se le envía uno nuevo. Sin enlace, la página muestra una demostración.

## Menú público para nuevos socios

`menu.html` muestra presentación, membresías, horarios por sede y un formulario de alta.

1. La persona completa el formulario y se le arma un mensaje de WhatsApp con un código de alta.
2. En el sistema, Socios > **Importar solicitud**: pegás el mensaje y queda en la lista.
3. **Aprobar y cobrar** la crea como socio "Pendiente de primer pago".
4. Al cobrar se le envía su app por WhatsApp.

## Importante

- Los comprobantes son internos y no tienen validez fiscal. La factura electrónica se emite en ARCA.
- Huella, NFC, molinete y la acreditación de Mercado Pago se simulan en la demo. En producción necesitan el lector conectado, un programa que lo conecte y la integración con la cuenta de Mercado Pago del gimnasio.
- El entrenador inteligente trabaja con reglas de entrenamiento; la rutina siempre la revisa y asigna un profesor.
- Los datos de cada navegador son locales: sin un servidor no hay sincronización en vivo entre dispositivos.
- Los datos, teléfonos y precios que trae son de demostración.

## Desarrollo

Sistema desarrollado por **Vincular Business**: digitalización, software de gestión y fidelización para comercios y servicios de Argentina.
WhatsApp (387) 4484132 · vincularbusiness@gmail.com
