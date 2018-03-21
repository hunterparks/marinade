import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TooltipContainerComponent } from './tooltip-container.component';

describe('TooltipContainerComponent', () => {
  let component: TooltipContainerComponent;
  let fixture: ComponentFixture<TooltipContainerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TooltipContainerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TooltipContainerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
