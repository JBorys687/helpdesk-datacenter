package ec.edu.utm.helpdesk.ticket;

import jakarta.persistence.*;
import java.time.Instant;

@Entity
@Table(name = "tickets")
public class Ticket {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @Column(nullable = false, length = 150)
    private String titulo;
    @Column(nullable = false, length = 2000)
    private String descripcion;
    @Enumerated(EnumType.STRING) @Column(nullable = false, length = 20)
    private Categoria categoria;
    @Enumerated(EnumType.STRING) @Column(nullable = false, length = 20)
    private Prioridad prioridad;
    @Enumerated(EnumType.STRING) @Column(nullable = false, length = 20)
    private Estado estado;
    @Column(nullable = false, updatable = false)
    private Instant creadoEn;
    @Column(nullable = false)
    private Instant actualizadoEn;

    protected Ticket() {}

    @PrePersist void antesDeCrear() {
        creadoEn = Instant.now(); actualizadoEn = creadoEn;
        if (estado == null) estado = Estado.ABIERTO;
    }
    @PreUpdate void antesDeActualizar() { actualizadoEn = Instant.now(); }

    public Long getId() { return id; }
    public String getTitulo() { return titulo; }
    public void setTitulo(String titulo) { this.titulo = titulo; }
    public String getDescripcion() { return descripcion; }
    public void setDescripcion(String descripcion) { this.descripcion = descripcion; }
    public Categoria getCategoria() { return categoria; }
    public void setCategoria(Categoria categoria) { this.categoria = categoria; }
    public Prioridad getPrioridad() { return prioridad; }
    public void setPrioridad(Prioridad prioridad) { this.prioridad = prioridad; }
    public Estado getEstado() { return estado; }
    public void setEstado(Estado estado) { this.estado = estado; }
    public Instant getCreadoEn() { return creadoEn; }
    public Instant getActualizadoEn() { return actualizadoEn; }
}
