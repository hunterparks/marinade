import { RouterModule, Routes } from '@angular/router';

import { EditorViewSidebarComponent } from './components/pages/editor-view/editor-view-sidebar/editor-view-sidebar.component';
import { EditorViewComponent } from './components/pages/editor-view/editor-view.component';
import { MemoryViewComponent } from './components/pages/memory-view/memory-view.component';
import { SettingsViewComponent } from './components/pages/settings-view/settings-view.component';
import { SimulatorViewSidebarComponent } from './components/pages/simulator-view/simulator-view-sidebar/simulator-view-sidebar.component';
import { SimulatorViewComponent } from './components/pages/simulator-view/simulator-view.component';

const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'editor' },
  {
    children: [
      { component: EditorViewComponent, path: '' },
      { component: EditorViewSidebarComponent, outlet: 'sidebar', path: '' },
    ],
    path: 'editor'
  },
  {
    children: [
      { component: SimulatorViewComponent, path: '' },
      { component: SimulatorViewSidebarComponent, outlet: 'sidebar', path: '' },
    ],
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
