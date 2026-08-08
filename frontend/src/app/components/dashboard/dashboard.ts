import { Component, inject, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { TicketService } from '../../services/ticket';
import { Ticket } from '../../models/ticket.model';

interface Conteo {
  etiqueta: string;
  valor: number;
}

@Component({
  selector: 'app-dashboard',
  imports: [RouterLink],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class Dashboard implements OnInit {
  private readonly ticketService = inject(TicketService);

  readonly cargando = signal(true);
  readonly error = signal(false);
  readonly tickets = signal<Ticket[]>([]);

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

  get total(): number {
    return this.tickets().length;
  }

  get porEstado(): Conteo[] {
    return this.contarPor((t) => t.estado, ['ABIERTO', 'EN_PROGRESO', 'CERRADO']);
  }

  get porCategoria(): Conteo[] {
    return this.contarPor((t) => t.categoria, ['RED', 'HARDWARE', 'SOFTWARE']);
  }

  get porPrioridad(): Conteo[] {
    return this.contarPor((t) => t.prioridad, ['ALTA', 'MEDIA', 'BAJA']);
  }

  get recientes(): Ticket[] {
    return [...this.tickets()]
      .sort((a, b) => new Date(b.creadoEn).getTime() - new Date(a.creadoEn).getTime())
      .slice(0, 5);
  }

  private contarPor(selector: (t: Ticket) => string, orden: string[]): Conteo[] {
    const tickets = this.tickets();
    return orden.map((etiqueta) => ({
      etiqueta,
      valor: tickets.filter((t) => selector(t) === etiqueta).length,
    }));
  }
}
