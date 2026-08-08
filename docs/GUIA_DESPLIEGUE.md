# Guía de despliegue en la nube — Actividad 9

Requisito de la actividad: base de datos remota, backend con URL pública y
frontend en hosting estático, sin depender de `localhost`.

## 1. Backend + base de datos en Render

El repositorio incluye [`render.yaml`](../render.yaml) (Blueprint), que crea
automáticamente:

- Una base de datos PostgreSQL gestionada (plan free).
- El servicio web del backend, construido desde el `Dockerfile` de la raíz,
  con las variables `DATABASE_HOST/PORT/NAME/USER/PASSWORD` ya conectadas a
  la base de datos anterior.

Pasos:

1. Ingresa a <https://dashboard.render.com/> con tu cuenta (crea una gratis
   si no tienes).
2. **New +** → **Blueprint** → conecta el repositorio
   `JBorys687/helpdesk-datacenter` (rama `develop`).
3. Render detecta `render.yaml` y muestra los dos recursos a crear
   (`helpdesk-datacenter-db` y `helpdesk-datacenter-api`). Antes de aplicar,
   completa las dos variables marcadas como secretas:
   - `SPRING_SECURITY_USER_NAME`: el usuario que usará el frontend para
     autenticarse (ej. `admin`).
   - `SPRING_SECURITY_USER_PASSWORD`: una contraseña robusta — **no la
     publiques en el informe ni en capturas**.
4. Aplica el Blueprint y espera a que el build termine (usa el `Dockerfile`,
   toma unos minutos la primera vez).
5. Copia la URL pública que Render asigna al servicio, con forma
   `https://helpdesk-datacenter-api.onrender.com` (puede variar el sufijo si
   el nombre ya estaba tomado).
6. Verifica que responde:
   ```bash
   curl -u TU_USUARIO:TU_CLAVE https://<tu-url>.onrender.com/tickets
   ```

> Nota: el plan free de Render "duerme" el servicio tras ~15 minutos sin
> tráfico; la primera petición después de inactividad puede tardar ~30-60s
> en responder. Es normal, coméntalo en las conclusiones del informe.

## 2. Frontend en Vercel

1. Actualiza `frontend/src/environments/environment.prod.ts` con la URL real
   obtenida en el paso anterior (`apiUrl`).
2. Con la [Vercel CLI](https://vercel.com/docs/cli) instalada:
   ```bash
   cd frontend
   npx vercel login          # autenticación por navegador, una sola vez
   npx vercel --prod         # despliega y muestra la URL pública
   ```
   O bien, sin CLI: en <https://vercel.com/new>, importa el mismo repositorio
   de GitHub, selecciona **Root Directory: `frontend`** — Vercel detecta la
   configuración desde `frontend/vercel.json` automáticamente.
3. Copia la URL pública (`https://<proyecto>.vercel.app`).

## 3. Cerrar el círculo: CORS

Una vez tengas la URL de Vercel, vuelve al dashboard de Render → el servicio
`helpdesk-datacenter-api` → **Environment** → edita `CORS_ALLOWED_ORIGINS`
con la URL real de Vercel (sin `/` final), por ejemplo:

```
https://helpdesk-datacenter.vercel.app
```

Guarda; Render reinicia el servicio automáticamente. Sin este paso, el
navegador bloqueará las peticiones del frontend por política CORS.

## 4. Verificación final

- Abre la URL de Vercel, inicia sesión con las credenciales configuradas en
  el paso 1.4, y confirma que el Dashboard carga datos reales.
- Crea, edita y elimina un ticket desde la interfaz pública (no localhost).
- Toma las capturas para el informe: Dashboard, Registro, Listado, y la
  tabla `tickets` con registros reales (puede verse desde el **Shell** de la
  base de datos en Render, pestaña *Connect*).
