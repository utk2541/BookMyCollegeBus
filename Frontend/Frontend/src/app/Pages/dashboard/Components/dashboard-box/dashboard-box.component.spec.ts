import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DashboardBoxComponent } from './dashboard-box.component';

describe('DashboardBoxComponent', () => {
  let component: DashboardBoxComponent;
  let fixture: ComponentFixture<DashboardBoxComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DashboardBoxComponent]
    });
    fixture = TestBed.createComponent(DashboardBoxComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
