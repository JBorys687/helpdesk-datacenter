// Modelo del dominio "Ticket", alineado con la entidad Ticket del backend
// (Actividad 8: ec.edu.utm.helpdesk.ticket.Ticket) para que el frontend y
// el backend compartan exactamente los mismos valores permitidos.

export type Categoria = 'RED' | 'HARDWARE' | 'SOFTWARE';
export type Prioridad = 'ALTA' | 'MEDIA' | 'BAJA';
export type Estado = 'ABIERTO' | 'EN_PROGRESO' | 'CERRADO';

export const CATEGORIAS: Categoria[] = ['RED', 'HARDWARE', 'SOFTWARE'];
export const PRIORIDADES: Prioridad[] = ['ALTA', 'MEDIA', 'BAJA'];
export const ESTADOS: Estado[] = ['ABIERTO', 'EN_PROGRESO', 'CERRADO'];

/** Ticket completo tal como lo devuelve la API (incluye id y timestamps). */
export interface Ticket {
  id: number;
  titulo: string;
  descripcion: string;
  categoria: Categoria;
  prioridad: Prioridad;
  estado: Estado;
  creadoEn: string;
  actualizadoEn: string;
}

/** Payload para crear/actualizar un ticket (sin id ni timestamps, los asigna el servidor). */
export interface TicketRequest {
  titulo: string;
  descripcion: string;
  categoria: Categoria;
  prioridad: Prioridad;
  estado: Estado;
}
