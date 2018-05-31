import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SimulatorViewSidebarComponent } from './simulator-view-sidebar.component';

describe('SimulatorViewSidebarComponent', () => {
  let component: SimulatorViewSidebarComponent;
  let fixture: ComponentFixture<SimulatorViewSidebarComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SimulatorViewSidebarComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SimulatorViewSidebarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
