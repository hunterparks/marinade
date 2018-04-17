import { RouterModule, Routes } from '@angular/router';

import { EditorViewComponent } from './components/pages/editor-view/editor-view.component';
import { MemoryViewComponent } from './components/pages/memory-view/memory-view.component';
import { SettingsViewComponent } from './components/pages/settings-view/settings-view.component';
import { SimulatorViewComponent } from './components/pages/simulator-view/simulator-view.component';

const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    redirectTo: 'editor'
  },
  {
    component: EditorViewComponent,
    path: 'editor'
  },
  {
    component: SimulatorViewComponent,
    path: 'simulator'
  },
  {
    component: MemoryViewComponent,
    path: 'memory'
  },
  {
    component: SettingsViewComponent,
    path: 'settings'
  }
];

export const marinadeRoutes: any = RouterModule.forRoot(routes, { useHash: true });
