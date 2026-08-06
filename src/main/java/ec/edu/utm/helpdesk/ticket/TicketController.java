package ec.edu.utm.helpdesk.ticket;

import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.net.URI;
import java.util.List;

@RestController
@RequestMapping("/tickets")
public class TicketController {
    private final TicketService service;
    public TicketController(TicketService service) { this.service = service; }

    @GetMapping public List<Ticket> listar() { return service.listar(); }
    @GetMapping("/{id}") public Ticket buscar(@PathVariable Long id) { return service.buscar(id); }

    @PostMapping
    public ResponseEntity<Ticket> crear(@Valid @RequestBody TicketRequest request) {
        Ticket creado = service.crear(request);
        return ResponseEntity.created(URI.create("/tickets/" + creado.getId())).body(creado);
    }

    @PutMapping("/{id}")
    public Ticket actualizar(@PathVariable Long id, @Valid @RequestBody TicketRequest request) {
        return service.actualizar(id, request);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> eliminar(@PathVariable Long id) {
        service.eliminar(id);
        return ResponseEntity.noContent().build();
    }
}
