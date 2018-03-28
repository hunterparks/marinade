import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';

import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatMenuModule } from '@angular/material/menu';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { CovalentHttpModule } from '@covalent/http';
import { CovalentHighlightModule } from '@covalent/highlight';
import { CovalentMarkdownModule } from '@covalent/markdown';
import { CovalentCodeEditorModule } from '@covalent/code-editor';
import { CovalentFileSelectModule } from '../platform/file-select';

import { AppComponent } from './app.component';
import { EditorViewComponent } from './editor-view/editor-view.component';
import { marinadeRoutingProviders, marinadeRoutes } from './app.routes';
import { SimulatorViewComponent } from './simulator-view/simulator-view.component';
import { MemoryViewComponent } from './memory-view/memory-view.component';
import { SettingsViewComponent } from './settings-view/settings-view.component';


@NgModule({
  declarations: [
    AppComponent,
    EditorViewComponent,
    SimulatorViewComponent,
    MemoryViewComponent,
    SettingsViewComponent
  ],
  imports: [
    BrowserModule,
    MatButtonModule,
    MatIconModule,
    MatButtonToggleModule,
    MatMenuModule,
    MatListModule,
    MatSidenavModule,
    CovalentHttpModule,
    CovalentHighlightModule,
    CovalentMarkdownModule,
    CovalentMarkdownModule,
    CovalentCodeEditorModule,
    CovalentFileSelectModule,
    BrowserAnimationsModule,
    marinadeRoutes
  ],
  providers: [
    marinadeRoutingProviders
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }
