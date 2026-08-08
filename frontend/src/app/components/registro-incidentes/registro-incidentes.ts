import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { TicketService } from '../../services/ticket';
import { CATEGORIAS, ESTADOS, PRIORIDADES } from '../../models/ticket.model';

@Component({
  selector: 'app-registro-incidentes',
  imports: [ReactiveFormsModule],
  templateUrl: './registro-incidentes.html',
  styleUrl: './registro-incidentes.css',
})
export class RegistroIncidentes {
  private readonly fb = inject(FormBuilder);
  private readonly ticketService = inject(TicketService);
  private readonly router = inject(Router);

  readonly categorias = CATEGORIAS;
  readonly prioridades = PRIORIDADES;
  readonly estados = ESTADOS;

  readonly enviando = signal(false);
  readonly error = signal<string | null>(null);
  readonly exito = signal(false);

  // Buena práctica de seguridad: se limita la longitud y se recorta el texto
  // (trim) antes de enviarlo. Angular, además, escapa por defecto cualquier
  // valor mostrado en las plantillas ({{ }}), lo que evita XSS al listar
  // estos mismos datos en el Dashboard y en el Listado de Tickets.
  readonly formulario = this.fb.nonNullable.group({
    titulo: ['', [Validators.required, Validators.maxLength(150)]],
    descripcion: ['', [Validators.required, Validators.maxLength(2000)]],
    categoria: [this.categorias[0], Validators.required],
    prioridad: [this.prioridades[1], Validators.required],
    estado: [this.estados[0], Validators.required],
  });

  enviar(): void {
    if (this.formulario.invalid) {
      this.formulario.markAllAsTouched();
      return;
    }

    const valores = this.formulario.getRawValue();
    const request = {
      ...valores,
      titulo: valores.titulo.trim(),
      descripcion: valores.descripcion.trim(),
    };

    this.enviando.set(true);
    this.error.set(null);
    this.ticketService.crear(request).subscribe({
      next: () => {
        this.enviando.set(false);
        this.exito.set(true);
        this.formulario.reset({
          titulo: '',
          descripcion: '',
          categoria: this.categorias[0],
          prioridad: this.prioridades[1],
          estado: this.estados[0],
        });
        setTimeout(() => this.exito.set(false), 4000);
      },
      error: () => {
        this.enviando.set(false);
        this.error.set('No se pudo registrar el incidente. Verifica los datos y la conexión con la API.');
      },
    });
  }

  irAListado(): void {
    this.router.navigate(['/listado']);
  }
}
