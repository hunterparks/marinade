import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MuxComponent } from './mux.component';

describe('MuxComponent', () => {
  let component: MuxComponent;
  let fixture: ComponentFixture<MuxComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MuxComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MuxComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
