import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StageRegisterComponent } from './stage-register.component';

describe('ControllerComponent', () => {
  let component: StageRegisterComponent;
  let fixture: ComponentFixture<StageRegisterComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StageRegisterComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StageRegisterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
