import { HttpClientModule } from '@angular/common/http';
import { ErrorHandler, NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import * as Raven from 'raven-js';
import { AppComponent } from './app.component';
import { BusComponent } from './components/common/simulator/bus/bus.component';
import { MuxComponent } from './components/common/simulator/mux/mux.component';
import { SimulatorComponent } from './components/pages/simulator/simulator.component';
import { SafeHtmlPipe } from './pipes/safe-html.pipe';
import { WebsocketService } from './services/websocket.service';
import { SentrySettings } from './settings/sentry/local.sentry.settings';
import { RegisterComponent } from './components/common/simulator/register/register.component';

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
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
  ],
  providers: [
    WebsocketService,
    // { provide: ErrorHandler, useClass: RavenErrorHandler }
  ]
})
export class AppModule { }
