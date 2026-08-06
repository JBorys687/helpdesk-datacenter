package ec.edu.utm.helpdesk.ticket;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public record TicketRequest(
        @NotBlank @Size(max = 150) String titulo,
        @NotBlank @Size(max = 2000) String descripcion,
        @NotNull Categoria categoria,
        @NotNull Prioridad prioridad,
        Estado estado) {}
