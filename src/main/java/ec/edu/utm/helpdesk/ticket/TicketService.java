package ec.edu.utm.helpdesk.ticket;

import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;

@Service
@Transactional(readOnly = true)
public class TicketService {
    private final TicketRepository repository;
    public TicketService(TicketRepository repository) { this.repository = repository; }

    public List<Ticket> listar() { return repository.findAll(Sort.by(Sort.Direction.DESC, "creadoEn")); }
    public Ticket buscar(Long id) { return repository.findById(id).orElseThrow(() -> new TicketNoEncontradoException(id)); }

    @Transactional
    public Ticket crear(TicketRequest request) {
        Ticket ticket = new Ticket();
        copiar(request, ticket);
        if (request.estado() == null) ticket.setEstado(Estado.ABIERTO);
        return repository.save(ticket);
    }

    @Transactional
    public Ticket actualizar(Long id, TicketRequest request) {
        Ticket ticket = buscar(id);
        copiar(request, ticket);
        if (request.estado() == null) ticket.setEstado(Estado.ABIERTO);
        return repository.save(ticket);
    }

    @Transactional
    public void eliminar(Long id) { repository.delete(buscar(id)); }

    private void copiar(TicketRequest request, Ticket ticket) {
        ticket.setTitulo(request.titulo().trim());
        ticket.setDescripcion(request.descripcion().trim());
        ticket.setCategoria(request.categoria());
        ticket.setPrioridad(request.prioridad());
        ticket.setEstado(request.estado());
    }
}
