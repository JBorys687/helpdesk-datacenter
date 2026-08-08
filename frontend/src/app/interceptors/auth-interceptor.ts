import { inject } from '@angular/core';
import { HttpInterceptorFn } from '@angular/common/http';
import { Auth } from '../services/auth';
import { environment } from '../../environments/environment';

/**
 * Adjunta la cabecera "Authorization: Basic ..." a toda petición dirigida a
 * la API del Help Desk, sin tocar peticiones a otros orígenes.
 */
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  if (!req.url.startsWith(environment.apiUrl)) {
    return next(req);
  }

  const auth = inject(Auth);
  const cabecera = auth.obtenerCabeceraBasic();
  if (!cabecera) {
    return next(req);
  }

  const clonada = req.clone({ setHeaders: { Authorization: cabecera } });
  return next(clonada);
};
