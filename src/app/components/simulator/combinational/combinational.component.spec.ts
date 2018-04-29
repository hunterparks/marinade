import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CombinationalComponent } from './combinational.component';

describe('CombinationalComponent', () => {
  let component: CombinationalComponent;
  let fixture: ComponentFixture<CombinationalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CombinationalComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CombinationalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
