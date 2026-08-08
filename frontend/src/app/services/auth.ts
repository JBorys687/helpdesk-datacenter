import { Service, signal } from '@angular/core';

const STORAGE_KEY = 'helpdesk_credenciales';

interface Credenciales {
  usuario: string;
  clave: string;
}

/**
 * Maneja la sesión HTTP Basic contra la API del backend (Actividad 8, Spring
 * Security). Buena práctica de seguridad: las credenciales solo se guardan en
 * sessionStorage (se borran al cerrar la pestaña), nunca en localStorage ni
 * en el código fuente, y jamás se registran en consola.
 */
@Service()
export class Auth {
  readonly autenticado = signal<boolean>(this.hayCredenciales());

  iniciarSesion(usuario: string, clave: string): void {
    const credenciales: Credenciales = { usuario: usuario.trim(), clave };
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(credenciales));
    this.autenticado.set(true);
  }

  cerrarSesion(): void {
    sessionStorage.removeItem(STORAGE_KEY);
    this.autenticado.set(false);
  }

  obtenerUsuario(): string | null {
    return this.leerCredenciales()?.usuario ?? null;
  }

  obtenerCabeceraBasic(): string | null {
    const credenciales = this.leerCredenciales();
    if (!credenciales) return null;
    const token = btoa(`${credenciales.usuario}:${credenciales.clave}`);
    return `Basic ${token}`;
  }

  private leerCredenciales(): Credenciales | null {
    const raw = sessionStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    try {
      return JSON.parse(raw) as Credenciales;
    } catch {
      return null;
    }
  }

  private hayCredenciales(): boolean {
    return this.leerCredenciales() !== null;
  }
}
