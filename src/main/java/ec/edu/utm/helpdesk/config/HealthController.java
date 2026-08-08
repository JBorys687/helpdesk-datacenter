package ec.edu.utm.helpdesk.config;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Endpoint público (sin autenticación) usado por el healthcheck de Render
 * para confirmar que el servicio está activo. No expone datos de la API.
 */
@RestController
public class HealthController {

    @GetMapping("/health")
    public ResponseEntity<Void> health() {
        return ResponseEntity.ok().build();
    }
}
