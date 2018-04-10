import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BusListItemComponent } from './bus-list-item.component';

describe('BusListItemComponent', () => {
  let component: BusListItemComponent;
  let fixture: ComponentFixture<BusListItemComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BusListItemComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BusListItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
