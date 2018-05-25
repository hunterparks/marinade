import { HttpClientModule } from '@angular/common/http';
import { ErrorHandler, NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CovalentCodeEditorModule } from '@covalent/code-editor';
import { CovalentHighlightModule } from '@covalent/highlight';
import { CovalentHttpModule } from '@covalent/http';
import { CovalentMarkdownModule } from '@covalent/markdown';
import * as Raven from 'raven-js';

import { PathComponent } from '@components/common/svg/path/path.component';
import { RectComponent } from '@components/common/svg/rect/rect.component';
import { TrapezoidComponent } from '@components/common/svg/trapezoid/trapezoid.component';
import { BusMonitorItemComponent } from '@components/simulator/bus-monitor/bus-monitor-item/bus-monitor-item.component';
import { BusMonitorComponent } from '@components/simulator/bus-monitor/bus-monitor.component';
import { AppComponent } from '@app/app.component';
import { marinadeRoutes } from '@app/app.routes';
import { CovalentFileSelectModule } from '@components/common/file-select/file-select/file-select.module';
import { TooltipContainerComponent } from '@components/common/tooltip/tooltip-container/tooltip-container.component';
import { TooltipComponent } from '@components/common/tooltip/tooltip-content/tooltip.component';
import { EditorViewSidebarComponent } from '@components/pages/editor-view/editor-view-sidebar/editor-view-sidebar.component';
import { EditorViewComponent } from '@components/pages/editor-view/editor-view.component';
import { MemoryViewComponent } from '@components/pages/memory-view/memory-view.component';
import { SettingsViewComponent } from '@components/pages/settings-view/settings-view.component';
import { SimulatorViewSidebarComponent } from '@components/pages/simulator-view/simulator-view-sidebar/simulator-view-sidebar.component';
import { SimulatorViewComponent } from '@components/pages/simulator-view/simulator-view.component';
import { TooltipDirective } from '@directives/tooltip/tooltip.directive';
import { EditorFileService } from '@services/editor/file/editor-file.service';
import { IpcService } from '@services/ipc/ipc.service';
import { ArchitectureService } from '@services/simulator/architecture/architecture.service';
import { BusMonitorService } from '@services/simulator/bus-monitor/bus-monitor.service';
import { RequestService } from '@services/simulator/request/request.service';
import { ResponseService } from '@services/simulator/response/response.service';
import { WebsocketService } from '@services/simulator/websocket/websocket.service';
import { TooltipService } from '@services/tooltip/tooltip.service';
// import { SentrySettings } from '@settings/sentry/local.sentry.settings';

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
    PathComponent,
    TrapezoidComponent,
    RectComponent,
    TooltipDirective,
    TooltipComponent,
    TooltipContainerComponent,
    EditorViewComponent,
    SimulatorViewComponent,
    MemoryViewComponent,
    SettingsViewComponent,
    BusMonitorComponent,
    BusMonitorItemComponent,
    SimulatorViewSidebarComponent,
    EditorViewSidebarComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    marinadeRoutes,
    BrowserAnimationsModule,
    CovalentFileSelectModule,
    CovalentCodeEditorModule,
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
    IpcService,
    EditorFileService,
    // { provide: ErrorHandler, useClass: RavenErrorHandler }
  ]
})
export class AppModule { }
