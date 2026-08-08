import { Component, computed, inject, OnInit, signal } from '@angular/core';
import { DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TicketService } from '../../services/ticket';
import { CATEGORIAS, Estado, ESTADOS, PRIORIDADES, Ticket } from '../../models/ticket.model';

@Component({
  selector: 'app-listado-tickets',
  imports: [FormsModule, DatePipe],
  templateUrl: './listado-tickets.html',
  styleUrl: './listado-tickets.css',
})
export class ListadoTickets implements OnInit {
  private readonly ticketService = inject(TicketService);

  readonly categorias = CATEGORIAS;
  readonly prioridades = PRIORIDADES;
  readonly estados = ESTADOS;

  readonly cargando = signal(true);
  readonly error = signal(false);
  readonly tickets = signal<Ticket[]>([]);
  readonly ticketEnEdicion = signal<number | null>(null);
  readonly estadoEnEdicion = signal<Estado>('ABIERTO');
  readonly ticketAEliminar = signal<Ticket | null>(null);

  filtroCategoria = signal<string>('TODAS');
  filtroEstado = signal<string>('TODOS');
  filtroTexto = signal<string>('');

  readonly ticketsFiltrados = computed(() => {
    const categoria = this.filtroCategoria();
    const estado = this.filtroEstado();
    const texto = this.filtroTexto().trim().toLowerCase();

    return this.tickets().filter((t) => {
      const coincideCategoria = categoria === 'TODAS' || t.categoria === categoria;
      const coincideEstado = estado === 'TODOS' || t.estado === estado;
      const coincideTexto = !texto || t.titulo.toLowerCase().includes(texto);
      return coincideCategoria && coincideEstado && coincideTexto;
    });
  });

  ngOnInit(): void {
    this.cargarTickets();
  }

  cargarTickets(): void {
    this.cargando.set(true);
    this.error.set(false);
    this.ticketService.listar().subscribe({
      next: (tickets) => {
        this.tickets.set(tickets);
        this.cargando.set(false);
      },
      error: () => {
        this.error.set(true);
        this.cargando.set(false);
      },
    });
  }

  editarEstado(ticket: Ticket): void {
    this.estadoEnEdicion.set(ticket.estado);
    this.ticketEnEdicion.set(ticket.id);
  }

  cancelarEdicion(): void {
    this.ticketEnEdicion.set(null);
  }

  guardarEstado(ticket: Ticket, nuevoEstado: Estado): void {
    const request = {
      titulo: ticket.titulo,
      descripcion: ticket.descripcion,
      categoria: ticket.categoria,
      prioridad: ticket.prioridad,
      estado: nuevoEstado,
    };
    this.ticketService.actualizar(ticket.id, request).subscribe({
      next: (actualizado) => {
        this.tickets.update((lista) => lista.map((t) => (t.id === actualizado.id ? actualizado : t)));
        this.ticketEnEdicion.set(null);
      },
      error: () => this.error.set(true),
    });
  }

  pedirConfirmacionEliminar(ticket: Ticket): void {
    this.ticketAEliminar.set(ticket);
  }

  cancelarEliminar(): void {
    this.ticketAEliminar.set(null);
  }

  confirmarEliminar(): void {
    const ticket = this.ticketAEliminar();
    if (!ticket) return;
    this.ticketService.eliminar(ticket.id).subscribe({
      next: () => {
        this.tickets.update((lista) => lista.filter((t) => t.id !== ticket.id));
        this.ticketAEliminar.set(null);
      },
      error: () => this.error.set(true),
    });
  }
}
