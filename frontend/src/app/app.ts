import { Component, inject } from '@angular/core';
import { RouterOutlet, Router, NavigationEnd } from '@angular/router';
import { Navegacion } from './components/navegacion/navegacion';
import { Auth } from './services/auth';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Navegacion],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  private readonly auth = inject(Auth);
  private readonly router = inject(Router);

  mostrarNavegacion = false;

  constructor() {
    this.router.events.subscribe((evento) => {
      if (evento instanceof NavigationEnd) {
        this.mostrarNavegacion = this.auth.autenticado() && !evento.urlAfterRedirects.startsWith('/login');
      }
    });
  }
}
