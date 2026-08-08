# Help Desk API — Actividad 8

Servicio REST para registrar y administrar incidentes. Desarrollado con Java 21,
Spring Boot, Spring Data JPA, Spring Security, PostgreSQL y Flyway.

## Funcionalidades

- `GET /tickets`: lista los incidentes.
- `GET /tickets/{id}`: obtiene un incidente.
- `POST /tickets`: crea un incidente y responde `201 Created`.
- `PUT /tickets/{id}`: actualiza todos los datos del incidente.
- `DELETE /tickets/{id}`: elimina el incidente y responde `204 No Content`.
- Validación de datos, respuestas de error JSON y autenticación HTTP Basic.
- Migración versionada para crear la tabla e índices de PostgreSQL.
- Pruebas automáticas del CRUD, validaciones y autenticación.

## Estructura

```text
src/main/java/.../ticket/   Entidad, DTO, repositorio, servicio y controlador
src/main/java/.../config/   Manejo global de errores
src/main/resources/         Configuración y migraciones de base de datos
src/test/                   Pruebas integrales con H2
docs/                       Colección Postman y guía de evidencias
```

## Requisitos

- Java 21
- Maven 3.6.3 o posterior
- Docker con Compose, o PostgreSQL instalado

## Ejecución local

Defina una contraseña únicamente en una variable de entorno; no la escriba en el
repositorio:

```bash
export DATABASE_PASSWORD='una-clave-local-segura'
docker compose up -d postgres
mvn spring-boot:run
```

Spring Security genera una contraseña temporal al arrancar. En la consola aparecerá
`Using generated security password`. El usuario es `user`. Copie la contraseña solo
para las pruebas locales y no la publique en las capturas.

También puede fijar credenciales mediante las variables estándar de Spring:

```bash
export SPRING_SECURITY_USER_NAME='operador'
export SPRING_SECURITY_USER_PASSWORD='una-clave-local-segura'
```

Variables disponibles:

| Variable | Valor predeterminado |
|---|---|
| `DATABASE_URL` | `jdbc:postgresql://localhost:5432/helpdesk` |
| `DATABASE_USER` | `helpdesk` |
| `DATABASE_PASSWORD` | Obligatoria |
| `PORT` | `8080` |

## Ejemplo con cURL

```bash
curl -u "$SPRING_SECURITY_USER_NAME:$SPRING_SECURITY_USER_PASSWORD" \
  -H 'Content-Type: application/json' \
  -d '{"titulo":"Falla de red","descripcion":"Sin conexión en laboratorio","categoria":"RED","prioridad":"ALTA","estado":"ABIERTO"}' \
  http://localhost:8080/tickets

curl -u "$SPRING_SECURITY_USER_NAME:$SPRING_SECURITY_USER_PASSWORD" \
  http://localhost:8080/tickets
```

Los valores válidos son:

- `categoria`: `RED`, `HARDWARE`, `SOFTWARE`.
- `prioridad`: `ALTA`, `MEDIA`, `BAJA`.
- `estado`: `ABIERTO`, `EN_PROGRESO`, `CERRADO`.

Los nombres se aceptan sin distinguir mayúsculas y minúsculas.

## Pruebas

```bash
mvn test
```

La colección [Postman](docs/HelpDesk.postman_collection.json) contiene las cinco
operaciones y guarda automáticamente el identificador del ticket creado.

## Flujo Git requerido por la actividad

Cuando se autorice la publicación:

```bash
git switch develop
git switch -c feature/backend-api
git add .
git commit -m "feat: implementar API REST de tickets"
git switch develop
git merge --no-ff feature/backend-api
git push origin develop feature/backend-api
```

Antes de entregar, añada al informe PDF el enlace del repositorio, capturas de las
respuestas `200`, `201` y `204`, el controlador principal y el resultado de `mvn test`.

## Actividad 9 — Frontend e integración Full Stack

El frontend (Angular 22, SPA) vive en [`frontend/`](frontend/README.md) y consume
esta misma API. Estructura del repositorio:

```text
/                    Backend (Actividad 8) — Java 21 / Spring Boot / PostgreSQL
frontend/            Frontend (Actividad 9) — Angular 22
render.yaml           Blueprint de despliegue del backend + BD en Render
frontend/vercel.json  Configuración de despliegue del frontend en Vercel
docs/                 Documentación, evidencias y guía de despliegue
```

### Despliegue en la nube

| Componente | Servicio | URL pública |
|---|---|---|
| Base de datos (PostgreSQL) | Render | interna (gestionada por Render) |
| Backend (API REST) | Render | _pendiente — se completa tras el despliegue_ |
| Frontend (SPA) | Vercel | _pendiente — se completa tras el despliegue_ |

Ver la guía paso a paso en [`docs/GUIA_DESPLIEGUE.md`](docs/GUIA_DESPLIEGUE.md).

### Flujo Git de esta actividad

```bash
git switch develop
git switch -c feature/frontend-app
# ... desarrollo del frontend ...
git switch develop
git merge --no-ff feature/frontend-app
git push origin develop feature/frontend-app
```
