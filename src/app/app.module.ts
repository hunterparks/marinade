import { HttpClientModule } from '@angular/common/http';
import { ErrorHandler, NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import * as Raven from 'raven-js';
import { AppComponent } from './app.component';
import { TooltipContainerComponent } from './components/common/tooltip/tooltip-container/tooltip-container.component';
import { TooltipComponent } from './components/common/tooltip/tooltip-content/tooltip.component';
import { SimulatorComponent } from './components/pages/simulator/simulator.component';
import { BusComponent } from './components/simulator/bus/bus.component';
import { ControllerComponent } from './components/simulator/controller/controller.component';
import { MuxComponent } from './components/simulator/mux/mux.component';
import { StageRegisterComponent } from './components/simulator/stage-register/stage-register.component';
import { StageComponent } from './components/simulator/stage/stage.component';
import { TooltipDirective } from './directives/tooltip/tooltip.directive';
import { SafeHtmlPipe } from './pipes/safe-html.pipe';
import { TransmitService } from './services/simulator/transmit/transmit.service';
import { WebsocketService } from './services/simulator/websocket/websocket.service';
import { TooltipService } from './services/tooltip/tooltip.service';
import { SentrySettings } from './settings/sentry/local.sentry.settings';

Raven.config(SentrySettings.getURL()).install();
Raven.setTagsContext({
  'Aspect': 'Frontend',
  'Language': 'TypeScript',
});

export class RavenErrorHandler implements ErrorHandler {
  public handleError(err: any): void {
    Raven.captureException(err);
  }
}

@NgModule({
  bootstrap: [AppComponent],
  declarations: [
    AppComponent,
    SimulatorComponent,
    SafeHtmlPipe,
    BusComponent,
    ControllerComponent,
    MuxComponent,
    StageComponent,
    StageRegisterComponent,
    TooltipDirective,
    TooltipComponent,
    TooltipContainerComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
  ],
  providers: [
    TooltipService,
    TransmitService,
    WebsocketService,
    // { provide: ErrorHandler, useClass: RavenErrorHandler }
  ]
})
export class AppModule { }
