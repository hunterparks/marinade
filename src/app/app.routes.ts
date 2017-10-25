import { Routes } from '@angular/router';
import { EditorComponent } from '@components/editor/editor.component';
import { MemoryComponent } from "@components/memory/memory.component";
import { SimulatorComponent } from "@components/simulator/simulator.component";

export const MarinadeRoutes: Routes = [
  { path: 'memory',    component: MemoryComponent },
  { path: 'simulator', component: SimulatorComponent },
  { path: '**',        component: EditorComponent }
];
