import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BusMonitorComponent } from './bus-monitor.component';

describe('BusTableComponent', () => {
  let component: BusMonitorComponent;
  let fixture: ComponentFixture<BusMonitorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BusMonitorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BusMonitorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
