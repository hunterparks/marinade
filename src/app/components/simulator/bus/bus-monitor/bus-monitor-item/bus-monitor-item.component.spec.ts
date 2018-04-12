import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BusMonitorItemComponent } from './bus-monitor-item.component';

describe('BusListItemComponent', () => {
  let component: BusMonitorItemComponent;
  let fixture: ComponentFixture<BusMonitorItemComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BusMonitorItemComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BusMonitorItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
