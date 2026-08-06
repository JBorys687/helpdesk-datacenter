package ec.edu.utm.helpdesk.ticket;

public class TicketNoEncontradoException extends RuntimeException {
    public TicketNoEncontradoException(Long id) { super("No existe el ticket con id " + id); }
}
