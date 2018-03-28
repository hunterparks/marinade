import { Routes, RouterModule } from '@angular/router';
import { EditorViewComponent } from './editor-view/editor-view.component';
import { SimulatorViewComponent } from './simulator-view/simulator-view.component';
import { MemoryViewComponent } from './memory-view/memory-view.component';
import { SettingsViewComponent } from './settings-view/settings-view.component';

const routes: Routes = [
  {
    redirectTo: 'editor',
    path: '',
    pathMatch: 'full'
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

export const marinadeRoutingProviders: any[] = [];

export const marinadeRoutes: any = RouterModule.forRoot(routes, { useHash: true });
