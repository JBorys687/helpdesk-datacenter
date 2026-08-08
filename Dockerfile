FROM maven:3.9.12-eclipse-temurin-21 AS build
WORKDIR /app
COPY pom.xml .
COPY src src
RUN mvn -q -DskipTests package

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /app/target/helpdesk-api-1.0.0.jar app.jar
# Render (servicios Docker) espera que el contenedor escuche en el puerto
# 10000 para su healthcheck/proxy interno. Se fija aquí para no depender de
# que la plataforma sincronice la variable PORT del Blueprint en cada deploy;
# application.yml sigue leyendo ${PORT} y localmente puede sobrescribirse
# con -e PORT=8080 si se prefiere ese puerto.
ENV PORT=10000
EXPOSE 10000
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
