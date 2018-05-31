import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EditorViewSidebarComponent } from '@components/pages/editor-view/editor-view-sidebar/editor-view-sidebar.component';

describe('EditorViewSidebarComponent', () => {
  let component: EditorViewSidebarComponent;
  let fixture: ComponentFixture<EditorViewSidebarComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EditorViewSidebarComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EditorViewSidebarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
