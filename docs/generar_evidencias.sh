#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
evidence_dir="$project_dir/docs/evidencias"
network_name="helpdesk-evidencias-net"
database_container="helpdesk-evidencias-db"
api_container="helpdesk-evidencias-api"
api_password="$(openssl rand -base64 24)"

cleanup() {
  docker rm -f "$api_container" "$database_container" >/dev/null 2>&1 || true
  docker network rm "$network_name" >/dev/null 2>&1 || true
}
trap cleanup EXIT

mkdir -p "$evidence_dir"
cleanup
docker network create "$network_name" >/dev/null
docker build -q -t helpdesk-api:evidencias "$project_dir" >/dev/null
docker run -d --name "$database_container" --network "$network_name" \
  -e POSTGRES_DB=helpdesk -e POSTGRES_USER=helpdesk \
  -e POSTGRES_HOST_AUTH_METHOD=trust postgres:17-alpine >/dev/null

for _ in $(seq 1 30); do
  docker exec "$database_container" pg_isready -U helpdesk -d helpdesk >/dev/null 2>&1 && break
  sleep 1
done

docker run -d --name "$api_container" --network "$network_name" -p 127.0.0.1:18080:8080 \
  -e DATABASE_URL=jdbc:postgresql://helpdesk-evidencias-db:5432/helpdesk \
  -e DATABASE_USER=helpdesk -e DATABASE_PASSWORD= \
  -e SPRING_SECURITY_USER_NAME=operador \
  -e SPRING_SECURITY_USER_PASSWORD="$api_password" helpdesk-api:evidencias >/dev/null

for _ in $(seq 1 60); do
  curl -fsS -u "operador:$api_password" http://127.0.0.1:18080/tickets >/dev/null 2>&1 && break
  sleep 1
done

request_create='{"titulo":"Falla de red en laboratorio","descripcion":"Los equipos no tienen acceso a Internet","categoria":"RED","prioridad":"ALTA","estado":"ABIERTO"}'
create_status="$(curl -sS -u "operador:$api_password" -o /tmp/helpdesk_create.json -w '%{http_code}' \
  -H 'Content-Type: application/json' -d "$request_create" http://127.0.0.1:18080/tickets)"
ticket_id="$(jq -r '.id' /tmp/helpdesk_create.json)"

list_status="$(curl -sS -u "operador:$api_password" -o /tmp/helpdesk_list.json -w '%{http_code}' http://127.0.0.1:18080/tickets)"
get_status="$(curl -sS -u "operador:$api_password" -o /tmp/helpdesk_get.json -w '%{http_code}' "http://127.0.0.1:18080/tickets/$ticket_id")"

request_update='{"titulo":"Falla de red en laboratorio","descripcion":"Conectividad restablecida y verificada","categoria":"RED","prioridad":"MEDIA","estado":"CERRADO"}'
update_status="$(curl -sS -u "operador:$api_password" -o /tmp/helpdesk_update.json -w '%{http_code}' \
  -X PUT -H 'Content-Type: application/json' -d "$request_update" "http://127.0.0.1:18080/tickets/$ticket_id")"
delete_status="$(curl -sS -u "operador:$api_password" -o /tmp/helpdesk_delete.json -w '%{http_code}' \
  -X DELETE "http://127.0.0.1:18080/tickets/$ticket_id")"

jq . /tmp/helpdesk_create.json > "$evidence_dir/01_crear_respuesta.json"
jq . /tmp/helpdesk_list.json > "$evidence_dir/02_listar_respuesta.json"
jq . /tmp/helpdesk_get.json > "$evidence_dir/03_buscar_respuesta.json"
jq . /tmp/helpdesk_update.json > "$evidence_dir/04_actualizar_respuesta.json"
printf '{"resultado":"Ticket eliminado correctamente"}\n' > "$evidence_dir/05_eliminar_respuesta.json"

printf '%s\n' "$create_status" "$list_status" "$get_status" "$update_status" "$delete_status" \
  > "$evidence_dir/estados_http.txt"

docker logs "$api_container" 2>&1 \
  | sed -E '/security password/d; /SPRING_SECURITY_USER_PASSWORD/d' \
  | tail -n 35 > "$evidence_dir/06_api_iniciada.txt"

printf 'Evidencias generadas: POST %s, GET lista %s, GET id %s, PUT %s, DELETE %s\n' \
  "$create_status" "$list_status" "$get_status" "$update_status" "$delete_status"
