import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListadoTickets } from './listado-tickets';

describe('ListadoTickets', () => {
  let component: ListadoTickets;
  let fixture: ComponentFixture<ListadoTickets>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListadoTickets],
    }).compileComponents();

    fixture = TestBed.createComponent(ListadoTickets);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
