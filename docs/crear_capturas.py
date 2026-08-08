#!/usr/bin/env python3
"""Crea páginas HTML imprimibles a partir de respuestas reales de la API."""
from html import escape
from pathlib import Path

BASE = Path(__file__).resolve().parent / "evidencias"

PRUEBAS = [
    ("01_crear", "POST", "/tickets", "201 Created", "01_crear_respuesta.json",
     '{"titulo":"Falla de red en laboratorio","descripcion":"Los equipos no tienen acceso a Internet","categoria":"RED","prioridad":"ALTA","estado":"ABIERTO"}'),
    ("02_listar", "GET", "/tickets", "200 OK", "02_listar_respuesta.json", None),
    ("03_buscar", "GET", "/tickets/1", "200 OK", "03_buscar_respuesta.json", None),
    ("04_actualizar", "PUT", "/tickets/1", "200 OK", "04_actualizar_respuesta.json",
     '{"titulo":"Falla de red en laboratorio","descripcion":"Conectividad restablecida y verificada","categoria":"RED","prioridad":"MEDIA","estado":"CERRADO"}'),
    ("05_eliminar", "DELETE", "/tickets/1", "204 No Content", "05_eliminar_respuesta.json", None),
]

STYLE = """
*{box-sizing:border-box} body{margin:0;background:#f3f6fa;font-family:Arial,sans-serif;color:#172033}
.top{height:72px;background:#172b4d;color:white;display:flex;align-items:center;padding:0 42px;font-size:24px;font-weight:bold}
.ok{margin-left:auto;background:#16855b;border-radius:18px;padding:8px 16px;font-size:15px}
.page{padding:32px 44px}.label{color:#52627a;font-size:14px;font-weight:bold;text-transform:uppercase;margin-bottom:8px}
.request{display:flex;background:white;border:1px solid #d8e0ea;border-radius:8px;overflow:hidden;margin-bottom:24px}
.method{padding:16px 22px;color:white;font-weight:bold;background:#2867d6}.url{padding:16px;font-family:monospace;font-size:17px}
.panel{background:#101723;color:#d7e4f2;border-radius:8px;padding:22px;margin-bottom:24px;box-shadow:0 3px 12px #ccd4df}
pre{margin:0;white-space:pre-wrap;font:15px/1.5 'DejaVu Sans Mono',monospace}.response{border-left:5px solid #20a06b}
.foot{color:#687890;font-size:13px;margin-top:18px}
"""

for name, method, endpoint, status, response_file, request_body in PRUEBAS:
    response = (BASE / response_file).read_text(encoding="utf-8").strip()
    body = ""
    if request_body:
        body = f'<div class="label">Cuerpo JSON enviado</div><div class="panel"><pre>{escape(request_body)}</pre></div>'
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{STYLE}</style></head>
<body><div class="top">Help Desk API — Prueba con cURL <span class="ok">HTTP {status}</span></div>
<main class="page"><div class="label">Petición autenticada</div><div class="request"><div class="method">{method}</div>
<div class="url">http://localhost:8080{endpoint}</div></div>{body}
<div class="label">Respuesta real de la API</div><div class="panel response"><pre>{escape(response)}</pre></div>
<div class="foot">Actividad 8 · Spring Boot · PostgreSQL · Respuesta capturada automáticamente el 6 de agosto de 2026</div>
</main></body></html>"""
    (BASE / f"{name}.html").write_text(html, encoding="utf-8")
