import { HttpClientModule } from '@angular/common/http';
import { ErrorHandler, NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import * as Raven from 'raven-js';
import { AppComponent } from './app.component';
import { BusComponent } from './components/common/simulator/bus/bus.component';
import { LabelComponent } from './components/common/simulator/label/label.component';
import { MuxComponent } from './components/common/simulator/mux/mux.component';
import { RegisterComponent } from './components/common/simulator/register/register.component';
import { TooltipContainerComponent } from './components/common/tooltip/tooltip-container/tooltip-container.component';
import { TooltipComponent } from './components/common/tooltip/tooltip-content/tooltip.component';
import { SimulatorComponent } from './components/pages/simulator/simulator.component';
import { TooltipDirective } from './directives/tooltip/tooltip.directive';
import { SafeHtmlPipe } from './pipes/safe-html.pipe';
import { WebsocketService } from './services/websocket.service';
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
    MuxComponent,
    BusComponent,
    RegisterComponent,
    LabelComponent,
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
    WebsocketService,
    // { provide: ErrorHandler, useClass: RavenErrorHandler }
  ]
})
export class AppModule { }
