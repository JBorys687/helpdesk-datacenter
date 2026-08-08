import { Component, inject, signal } from '@angular/core';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';
import { Auth } from '../../services/auth';

@Component({
  selector: 'app-navegacion',
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './navegacion.html',
  styleUrl: './navegacion.css',
})
export class Navegacion {
  private readonly auth = inject(Auth);
  private readonly router = inject(Router);

  readonly menuAbierto = signal(false);
  readonly usuario = this.auth.obtenerUsuario();

  alternarMenu(): void {
    this.menuAbierto.update((valor) => !valor);
  }

  cerrarMenu(): void {
    this.menuAbierto.set(false);
  }

  salir(): void {
    this.auth.cerrarSesion();
    this.cerrarMenu();
    this.router.navigate(['/login']);
  }
}
