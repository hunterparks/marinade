import { HttpClientModule } from '@angular/common/http';
import { ErrorHandler, NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { MatMenuModule } from '@angular/material/menu';
import { MatSidenavModule } from '@angular/material/sidenav';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CovalentCodeEditorModule } from '@covalent/code-editor';
import { CovalentHighlightModule } from '@covalent/highlight';
import { CovalentHttpModule } from '@covalent/http';
import { CovalentMarkdownModule } from '@covalent/markdown';
import * as Raven from 'raven-js';

import { AppComponent } from './app.component';
import { marinadeRoutes } from './app.routes';
import { CovalentFileSelectModule } from './components/common/file-select/file-select/file-select.module';
import { TooltipContainerComponent } from './components/common/tooltip/tooltip-container/tooltip-container.component';
import { TooltipComponent } from './components/common/tooltip/tooltip-content/tooltip.component';
import { EditorViewComponent } from './components/pages/editor-view/editor-view.component';
import { MemoryViewComponent } from './components/pages/memory-view/memory-view.component';
import { SettingsViewComponent } from './components/pages/settings-view/settings-view.component';
import { SimulatorViewComponent } from './components/pages/simulator-view/simulator-view.component';
import { BusMonitorItemComponent } from './components/simulator/bus/bus-monitor/bus-monitor-item/bus-monitor-item.component';
import { BusMonitorComponent } from './components/simulator/bus/bus-monitor/bus-monitor.component';
import { BusComponent } from './components/simulator/bus/bus/bus.component';
import { ControllerComponent } from './components/simulator/controller/controller.component';
import { MuxComponent } from './components/simulator/mux/mux.component';
import { StageRegisterComponent } from './components/simulator/stage-register/stage-register.component';
import { StageComponent } from './components/simulator/stage/stage.component';
import { TooltipDirective } from './directives/tooltip/tooltip.directive';
import { SafeHtmlPipe } from './pipes/safe-html.pipe';
import { BusMonitorService } from './services/simulator/bus-monitor/bus-monitor.service';
import { ArchitectureService } from './services/simulator/architecture/architecture.service';
import { ResponseService } from './services/simulator/response/response.service';
import { RequestService } from './services/simulator/request/request.service';
import { WebsocketService } from './services/simulator/websocket/websocket.service';
import { TooltipService } from './services/tooltip/tooltip.service';
import { SentrySettings } from './settings/sentry/local.sentry.settings';

// Raven.config(SentrySettings.getURL()).install();
// Raven.setTagsContext({
//   'Aspect': 'Frontend',
//   'Language': 'TypeScript',
// });

// export class RavenErrorHandler implements ErrorHandler {
//   public handleError(err: any): void {
//     Raven.captureException(err);
//   }
// }

@NgModule({
  bootstrap: [AppComponent],
  declarations: [
    AppComponent,
    SimulatorViewComponent,
    SafeHtmlPipe,
    BusComponent,
    ControllerComponent,
    MuxComponent,
    StageComponent,
    StageRegisterComponent,
    TooltipDirective,
    TooltipComponent,
    TooltipContainerComponent,
    EditorViewComponent,
    SimulatorViewComponent,
    MemoryViewComponent,
    SettingsViewComponent,
    BusMonitorComponent,
    BusMonitorItemComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    marinadeRoutes,
    BrowserAnimationsModule,
    CovalentFileSelectModule,
    CovalentCodeEditorModule,
    MatButtonModule,
    MatIconModule,
    MatButtonToggleModule,
    MatMenuModule,
    MatListModule,
    MatSidenavModule,
    CovalentHttpModule,
    CovalentHighlightModule,
    CovalentMarkdownModule,
  ],
  providers: [
    BusMonitorService,
    ArchitectureService,
    ResponseService,
    TooltipService,
    RequestService,
    WebsocketService,
    // { provide: ErrorHandler, useClass: RavenErrorHandler }
  ]
})
export class AppModule { }
