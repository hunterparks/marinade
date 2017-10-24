import { Routes } from '@angular/router';
import { EditorComponent } from '@components/editor/editor.component';

export const MarinadeRoutes: Routes = [
  {path: '**', component: EditorComponent}
];
