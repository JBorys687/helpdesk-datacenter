# Help Desk UTM — Frontend (Actividad 9)

Single Page Application en **Angular 22** para el Sistema de Gestión de
Incidentes (Help Desk). Consume la API REST desarrollada en la
Actividad 8 (backend Spring Boot, en la raíz de este repositorio).

## Componentes

| Componente | Ruta | Responsabilidad |
|---|---|---|
| `Navegacion` | (barra fija) | Menú principal y cierre de sesión |
| `Login` | `/login` | Ingreso de credenciales HTTP Basic contra la API |
| `Dashboard` | `/dashboard` | KPIs, conteos por categoría/prioridad/estado, últimos tickets |
| `RegistroIncidentes` | `/registro` | Formulario reactivo para crear tickets |
| `ListadoTickets` | `/listado` | Tabla con filtros, edición de estado y eliminación |

## Arquitectura de datos

- `services/ticket.ts` (`TicketService`): los 5 endpoints REST (`GET /tickets`,
  `GET /tickets/{id}`, `POST`, `PUT`, `DELETE`) mediante `HttpClient`.
- `services/auth.ts` (`Auth`): guarda las credenciales HTTP Basic en
  `sessionStorage` (no en `localStorage`, se pierden al cerrar la pestaña).
- `interceptors/auth-interceptor.ts`: agrega la cabecera `Authorization` solo
  a las peticiones dirigidas a la API configurada en `environment.ts`.
- `guards/auth-guard.ts`: bloquea el acceso a las rutas internas sin sesión.

## Buenas prácticas de seguridad (requisito de la actividad)

- **Prevención de XSS**: Angular escapa automáticamente cualquier valor
  interpolado en las plantillas (`{{ }}`); el proyecto no usa `[innerHTML]`
  en ningún componente, por lo que el contenido ingresado por el usuario
  (título, descripción) nunca se interpreta como HTML/JS.
- Los campos de texto se recortan (`trim`) y limitan en longitud
  (`Validators.maxLength`) antes de enviarse al backend.
- Las credenciales nunca se escriben en el código fuente ni se registran en
  consola; viven únicamente en `sessionStorage` del navegador del usuario.

## Configuración de entornos

| Archivo | Uso | `apiUrl` |
|---|---|---|
| `src/environments/environment.ts` | `ng serve` (desarrollo) | `http://localhost:8080` |
| `src/environments/environment.prod.ts` | `ng build --configuration production` | URL pública del backend en Render |

## Ejecución local

```bash
npm install
npm start          # http://localhost:4200, requiere el backend corriendo en :8080
```

## Build de producción

```bash
npm run build       # usa environment.prod.ts (ver angular.json → fileReplacements)
# genera dist/frontend/browser, listo para servir como sitio estático
```

## Despliegue

Publicado como sitio estático en **Vercel** (ver `vercel.json` en la raíz del
repositorio y la guía de despliegue en `docs/GUIA_DESPLIEGUE.md`).
