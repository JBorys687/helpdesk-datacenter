# Evidencias para el informe PDF

1. Portada usando el formato institucional.
2. Breve explicación de Java, Spring Boot, PostgreSQL, JPA y Flyway.
3. Captura de la tabla `tickets` creada por la migración.
4. Capturas de Postman para crear, listar, buscar, actualizar y eliminar.
5. En cada captura debe verse el método, URL, estado HTTP y JSON, pero no claves.
6. Captura de `mvn test` con todas las pruebas aprobadas.
7. Fragmento de `TicketController.java`.
8. Enlace al repositorio y evidencia de las ramas `feature/backend-api` y `develop`.

Estados esperados: `200 OK` al consultar/actualizar, `201 Created` al crear y
`204 No Content` al eliminar. Una consulta inexistente debe responder `404`.
