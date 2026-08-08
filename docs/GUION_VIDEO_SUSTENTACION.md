# Guion — Video de sustentación (Actividad 9)

Requisito obligatorio: 5–10 minutos, mostrando tu rostro, sin restricciones de
acceso al subirlo (Drive/YouTube/Loom). Si falta, se anula toda la actividad.

Graba con Zoom, OBS, o el grabador de pantalla del sistema (con cámara web
activa en una esquina). Sugerencia de estructura y tiempos:

## 1. Presentación (0:00–0:45)

- Muestra tu rostro y preséntate: nombre completo, materia (Desarrollo de
  Sistemas Informáticos), actividad (# 9), fecha.
- Una frase de qué vas a mostrar: "Voy a presentar el Sistema de Gestión de
  Incidentes Help Desk, con su frontend en Angular, backend en Spring Boot y
  despliegue completo en la nube."

## 2. Arquitectura del sistema (0:45–2:30)

- Comparte pantalla con el diagrama cliente/servidor (`docs/evidencias9/diagrama_arquitectura.png`
  o la imagen en el informe).
- Explica en tus palabras (no leas literal):
  - El **frontend** (Angular 22) corre como sitio estático en Vercel y
    consume la API por HTTP.
  - El **backend** (Spring Boot) expone los 5 endpoints REST sobre `/tickets`
    y corre en un contenedor Docker en Render.
  - La **base de datos** (PostgreSQL) vive en Render, separada del backend.
  - Autenticación HTTP Basic entre frontend y backend.

## 3. Código fuente principal (2:30–5:00)

Abre el editor y muestra, sin leer línea por línea, solo explicando qué hace:

- `TicketController.java`: los 5 endpoints CRUD.
- `SecurityConfig.java`: HTTP Basic + CORS (por qué es necesario: frontend y
  backend están en dominios distintos).
- Frontend: `ticket.ts` (servicio HTTP), `dashboard.ts` (cómo calcula los
  KPIs), y uno de los componentes visuales (`registro-incidentes.ts` o
  `listado-tickets.ts`).
- Menciona brevemente la prevención de XSS (Angular escapa automáticamente
  el contenido interpolado) y que las credenciales solo viven en
  `sessionStorage`.

## 4. Proceso de despliegue (5:00–6:30)

- Muestra el dashboard de Render: el Blueprint, el servicio web y la base de
  datos, y las variables de entorno (sin mostrar la contraseña en pantalla).
- Muestra el proyecto en Vercel: el último deploy y su URL pública.
- Opcional: muestra brevemente `render.yaml` y `frontend/vercel.json` en el
  repositorio.

## 5. Demostración en vivo (6:30–9:00)

Desde la **URL pública** (no localhost):

1. Abre el sitio, inicia sesión.
2. Dashboard: muestra los KPIs con datos reales.
3. Registro de Incidentes: crea un ticket nuevo en vivo.
4. Listado de Tickets: ubica el ticket creado, cambia su estado (por ejemplo
   a "En Progreso"), y muéstralo actualizado.
5. Elimina un ticket y muestra que desaparece de la lista.
6. (Opcional) Recarga la página para demostrar que los datos persisten en la
   base de datos remota, no en memoria local.

## 6. Cierre (9:00–10:00)

- Menciona 1–2 conclusiones técnicas: qué aprendiste del proceso de
  integración full-stack y del despliegue en la nube (por ejemplo, la
  configuración de CORS entre dominios distintos, o la latencia del primer
  request en el plan gratuito de Render).
- Agradece y cierra mostrando tu rostro nuevamente.

## Antes de subir el video

- Revisa que no aparezca ninguna contraseña, token o variable de entorno en
  pantalla durante la grabación.
- Sube a Drive/YouTube/Loom y **verifica en una ventana de incógnito** que
  cualquier persona con el enlace puede reproducirlo sin iniciar sesión.
