import { Routes } from '@angular/router';
import { authGuard } from './guards/auth-guard';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'dashboard' },
  {
    path: 'login',
    loadComponent: () => import('./components/login/login').then((m) => m.Login),
  },
  {
    path: 'dashboard',
    canActivate: [authGuard],
    loadComponent: () => import('./components/dashboard/dashboard').then((m) => m.Dashboard),
  },
  {
    path: 'registro',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./components/registro-incidentes/registro-incidentes').then((m) => m.RegistroIncidentes),
  },
  {
    path: 'listado',
    canActivate: [authGuard],
    loadComponent: () => import('./components/listado-tickets/listado-tickets').then((m) => m.ListadoTickets),
  },
  { path: '**', redirectTo: 'dashboard' },
];
