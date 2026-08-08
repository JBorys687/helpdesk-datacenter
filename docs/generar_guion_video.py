#!/usr/bin/env python3
"""Genera un documento Word detallado del guion de video (Actividad 9),
con URLs y rutas de archivo exactas para saber qué pantalla mostrar en
cada momento."""
from pathlib import Path
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Pt, RGBColor, Inches

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/Guion_Video_Sustentacion_Actividad_9.docx"

VERDE = RGBColor(0x1F, 0x6B, 0x3A)
VERDE_OSC = RGBColor(0x15, 0x4D, 0x29)
ROJO = RGBColor(0xC0, 0x39, 0x2B)
GRIS = RGBColor(0x5A, 0x6B, 0x60)

doc = Document()
styles = doc.styles
styles["Normal"].font.name = "Arial"
styles["Normal"].font.size = Pt(11)

section = doc.sections[0]
section.left_margin = Inches(0.9)
section.right_margin = Inches(0.9)


def h1(texto):
    p = doc.add_paragraph()
    r = p.add_run(texto)
    r.bold = True
    r.font.size = Pt(18)
    r.font.color.rgb = VERDE_OSC
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(10)
    return p


def h2(texto):
    p = doc.add_paragraph()
    r = p.add_run(texto)
    r.bold = True
    r.font.size = Pt(14)
    r.font.color.rgb = VERDE
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    borde = doc.add_paragraph()  # spacer invisible, se quita luego si molesta
    borde._p.getparent().remove(borde._p)
    return p


def parrafo(texto, negrita=False, color=None, italic=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(texto)
    r.bold = negrita
    r.italic = italic
    if color:
        r.font.color.rgb = color
    return p


def vineta(texto, nivel=0):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.3 + 0.25 * nivel)
    p.paragraph_format.first_line_indent = Inches(-0.18)
    p.add_run("• ").bold = True
    p.add_run(texto)
    return p


def caja_aviso(titulo_txt, texto, color=VERDE):
    tabla = doc.add_table(rows=1, cols=1)
    tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
    celda = tabla.rows[0].cells[0]
    celda.text = ""
    p = celda.paragraphs[0]
    r = p.add_run(f"{titulo_txt}\n")
    r.bold = True
    r.font.color.rgb = color
    r2 = p.add_run(texto)
    r2.font.size = Pt(10)
    doc.add_paragraph()
    return tabla


def tabla_pasos(filas, encabezados=("Tiempo", "Pantalla / URL exacta", "Qué decir / hacer")):
    tabla = doc.add_table(rows=1, cols=len(encabezados))
    tabla.style = "Table Grid"
    tabla.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, texto in enumerate(encabezados):
        celda = tabla.rows[0].cells[i]
        celda.text = texto
        celda.paragraphs[0].runs[0].bold = True
    widths = [Inches(0.8), Inches(2.3), Inches(3.4)]
    for fila in filas:
        cells = tabla.add_row().cells
        for i, valor in enumerate(fila):
            cells[i].text = valor
    for row in tabla.rows:
        for i, cell in enumerate(row.cells):
            if i < len(widths):
                cell.width = widths[i]
    doc.add_paragraph()
    return tabla


# ───────────────────────────── Portada simple ─────────────────────────────
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("UNIVERSIDAD TÉCNICA DE MANABÍ")
r.bold = True
r.font.size = Pt(12)
r.font.color.rgb = GRIS

h1("Guion del Video de Sustentación — Actividad #9")
parrafo("Desarrollo de Sistemas Informáticos · Sistema de Gestión de Incidentes (Help Desk)", italic=True, color=GRIS)
parrafo("Duración recomendada: 5 a 10 minutos. Debe mostrar tu rostro en todo momento (webcam encendida) y grabar tu voz explicando, no leyendo un guion palabra por palabra.")

caja_aviso(
    "⚠ REQUISITO OBLIGATORIO",
    "Si el video falta, se anula automáticamente la calificación de TODA la actividad #9 "
    "(no solo la parte del video). Debe subirse a Drive, YouTube o Loom SIN restricción de acceso "
    "— pruébalo en una ventana de incógnito antes de entregar.",
    ROJO,
)

h2("Qué necesitas abierto ANTES de darle 'Grabar'")
vineta("Tu cámara y micrófono funcionando (pruébalos primero).")
vineta("Programa de grabación: Zoom, OBS Studio, o el grabador de pantalla de Windows/Mac con webcam en una esquina.")
vineta("Pestañas del navegador abiertas de antemano, en este orden (así no pierdes tiempo buscando durante la grabación):")
vineta("Pestaña 1 — Diagrama de arquitectura: abre docs/evidencias9/diagrama_arquitectura.png (está en el repositorio) o la página 3 del informe PDF.", 1)
vineta("Pestaña 2 — Repositorio en GitHub: https://github.com/JBorys687/helpdesk-datacenter", 1)
vineta("Pestaña 3 — Panel de Render: https://dashboard.render.com (proyecto helpdesk-datacenter-api)", 1)
vineta("Pestaña 4 — Panel de Vercel: https://vercel.com/borys5/helpdesk-datacenter", 1)
vineta("Pestaña 5 — El sistema en vivo: https://helpdesk-datacenter-blush.vercel.app (cierra sesión antes de empezar, para hacer el login en cámara)", 1)
vineta("Ten a mano tu usuario y contraseña de la API (los que pusiste en Render) para iniciar sesión en vivo.")

caja_aviso(
    "🔒 Antes de grabar la pantalla de Render",
    "En la pestaña Environment de Render, oculta o evita mostrar el valor de SPRING_SECURITY_USER_PASSWORD "
    "(hay un ícono de 'ojo' para ocultarlo). No debe quedar visible en el video.",
    VERDE_OSC,
)

# ───────────────────────────── Guion minuto a minuto ─────────────────────────────
h1("Guion minuto a minuto")

h2("1. Presentación — 0:00 a 0:45  (solo tu cámara, sin compartir pantalla todavía)")
tabla_pasos([
    ("0:00", "Solo tu rostro (webcam)", "Mira a la cámara y di: tu nombre completo, que cursas Desarrollo de Sistemas Informáticos, "
     "y que vas a presentar la Actividad 9: el Sistema de Gestión de Incidentes (Help Desk), con frontend Angular, "
     "backend Spring Boot y despliegue en la nube."),
])

h2("2. Arquitectura del sistema — 0:45 a 2:30  (comparte pantalla: Pestaña 1)")
tabla_pasos([
    ("0:45", "Imagen: docs/evidencias9/diagrama_arquitectura.png\n(o página 3 del PDF de entrega)",
     "Señala cada caja del diagrama mientras hablas:\n"
     "• El navegador del usuario llama por HTTPS al Frontend Angular, alojado como sitio estático en Vercel.\n"
     "• El Frontend consume la API REST del Backend Spring Boot, alojado en Render dentro de un contenedor Docker.\n"
     "• El Backend guarda todo en PostgreSQL, también en Render, en un servidor separado.\n"
     "• La autenticación entre Frontend y Backend es HTTP Basic."),
])

h2("3. Código fuente principal — 2:30 a 5:00  (comparte pantalla: Pestaña 2, GitHub)")
parrafo("Navega directamente a estas URLs (o abre los mismos archivos en tu editor local) y explica brevemente qué hace cada uno, sin leer el código línea por línea:")
tabla_pasos([
    ("2:30", "https://github.com/JBorys687/helpdesk-datacenter/blob/main/src/main/java/ec/edu/utm/helpdesk/ticket/TicketController.java",
     "\"Este es el controlador REST del backend: expone los 5 endpoints — GET /tickets, GET /tickets/{id}, "
     "POST, PUT y DELETE — que gestionan los incidentes.\""),
    ("3:15", "https://github.com/JBorys687/helpdesk-datacenter/blob/main/src/main/java/ec/edu/utm/helpdesk/config/SecurityConfig.java",
     "\"Aquí configuro la seguridad: autenticación HTTP Basic obligatoria en toda la API, y CORS para que "
     "solo mi frontend en Vercel pueda hacerle peticiones al backend.\""),
    ("4:00", "https://github.com/JBorys687/helpdesk-datacenter/blob/main/frontend/src/app/services/ticket.ts",
     "\"En el frontend, este servicio centraliza las llamadas HTTP a la API — listar, crear, actualizar y "
     "eliminar tickets — usando HttpClient de Angular.\""),
    ("4:30", "https://github.com/JBorys687/helpdesk-datacenter/blob/main/frontend/src/app/components/dashboard/dashboard.ts",
     "\"El componente Dashboard calcula los KPIs (total de tickets, por estado, por categoría, por prioridad) "
     "en el propio navegador a partir de los datos que trae la API.\""),
], encabezados=("Tiempo", "Archivo / URL exacta", "Qué decir"))

h2("4. Proceso de despliegue — 5:00 a 6:30  (comparte pantalla: Pestañas 3 y 4)")
tabla_pasos([
    ("5:00", "https://dashboard.render.com → proyecto helpdesk-datacenter-api → pestaña 'Events'",
     "\"Este es el backend desplegado en Render, construido desde un Dockerfile. Aquí se ven los despliegues "
     "y el estado 'Live'.\" Muestra también la pestaña Environment (con la contraseña oculta) para explicar "
     "las variables de entorno (base de datos, CORS)."),
    ("5:45", "https://vercel.com/borys5/helpdesk-datacenter → Overview",
     "\"Y este es el frontend Angular, publicado como sitio estático en Vercel. Cada vez que subo cambios al "
     "repositorio, se despliega automáticamente.\" Señala la URL de producción visible en la pantalla."),
])

h2("5. Demostración en vivo — 6:30 a 9:00  (comparte pantalla: Pestaña 5, LA URL PÚBLICA, no localhost)")
tabla_pasos([
    ("6:30", "https://helpdesk-datacenter-blush.vercel.app/login",
     "Escribe tu usuario y contraseña en cámara e inicia sesión. Di: \"Esta es la URL pública real, no estoy "
     "usando mi computador como servidor.\""),
    ("7:00", "Pestaña 'Dashboard' (menú superior)",
     "\"Aquí veo el resumen: total de tickets, cuántos están abiertos, en progreso o cerrados, y el desglose "
     "por categoría y prioridad, todo calculado con datos reales de la base de datos.\""),
    ("7:30", "Pestaña 'Registrar Incidente'",
     "Llena el formulario en vivo (título, descripción, categoría, prioridad, estado) y dale clic en "
     "'Registrar incidente'. Espera el mensaje de éxito en pantalla."),
    ("8:00", "Pestaña 'Listado de Tickets'",
     "Muestra que el ticket recién creado aparece en la tabla. Dale clic al ícono de lápiz (✏️), cambia el "
     "estado (por ejemplo a 'En Progreso') y guarda con el ícono de disquete (💾)."),
    ("8:30", "Misma pantalla — Listado de Tickets",
     "Dale clic al ícono de basura (🗑️) de ese ticket, confirma la eliminación en el cuadro que aparece, y "
     "muestra que desaparece de la lista. \"Con esto demuestro el CRUD completo: crear, leer, actualizar y "
     "eliminar, funcionando 100% en producción.\""),
])

h2("6. Cierre — 9:00 a 10:00  (vuelve a mostrar solo tu cámara)")
tabla_pasos([
    ("9:00", "Solo tu rostro (webcam)",
     "Menciona 1 o 2 conclusiones técnicas propias, por ejemplo: lo que aprendiste al configurar CORS entre "
     "dominios distintos, o la demora del primer request en el plan gratuito de Render (el servicio 'duerme' "
     "tras ~15 min sin uso). Agradece y despídete mirando a la cámara."),
], encabezados=("Tiempo", "Pantalla", "Qué decir"))

doc.add_page_break()

h1("Checklist final antes de subir el video")
vineta("¿Se ve tu rostro claramente al inicio y al final?")
vineta("¿Mencionaste tu nombre completo y la actividad?")
vineta("¿Mostraste el diagrama de arquitectura y explicaste los 3 componentes (frontend/backend/BD)?")
vineta("¿Mostraste al menos 3 archivos de código (backend y frontend)?")
vineta("¿Mostraste Render y Vercel con los servicios 'Live'/desplegados?")
vineta("¿Hiciste login, creaste, actualizaste y eliminaste un ticket, todo desde la URL pública (no localhost)?")
vineta("¿Ninguna contraseña quedó visible en pantalla?")
vineta("¿Subiste el video a Drive/YouTube/Loom y lo probaste en una ventana de incógnito (sin iniciar sesión)?")

parrafo("")
parrafo(
    "Una vez tengas el enlace del video, agrégalo en el informe de entrega (sección 'Sustentación en video') "
    "y en la plataforma junto con el resto de los enlaces.",
    italic=True, color=GRIS,
)

doc.save(OUTPUT)
print(OUTPUT)
