import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from '@app/app.component';
import { ProjectTreeComponent } from '@components/editor/project-tree/project-tree.component';
import { TreeNodeComponent } from '@components/editor/project-tree/tree-node/tree-node.component';
import { MenuBarComponent } from '@components/common/layout/menu-bar/menu-bar.component';
import { RouterModule } from '@angular/router';
import { MarinadeRoutes } from '@app/app.routes';
import { EditorComponent } from '@components/editor/editor.component';
import { MemoryComponent } from '@components/memory/memory.component';
import { SimulatorComponent } from '@components/simulator/simulator.component';
import { AceEditorModule } from 'ng2-ace-editor';

@NgModule({
  declarations: [
    AppComponent,
    ProjectTreeComponent,
    TreeNodeComponent,
    MenuBarComponent,
    EditorComponent,
    MemoryComponent,
    SimulatorComponent
  ],
  imports: [
    AceEditorModule,
    BrowserModule,
    RouterModule.forRoot(MarinadeRoutes),
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
