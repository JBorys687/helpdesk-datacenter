import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { Auth } from '../services/auth';

/** Bloquea el acceso a las rutas protegidas si no hay credenciales guardadas. */
export const authGuard: CanActivateFn = () => {
  const auth = inject(Auth);
  const router = inject(Router);

  if (auth.autenticado()) {
    return true;
  }

  router.navigate(['/login']);
  return false;
};
