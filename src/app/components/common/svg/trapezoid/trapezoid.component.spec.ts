import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TrapezoidComponent } from './trapezoid.component';

describe('MuxComponent', () => {
  let component: TrapezoidComponent;
  let fixture: ComponentFixture<TrapezoidComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TrapezoidComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TrapezoidComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
