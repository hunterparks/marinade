import { HttpClientModule } from '@angular/common/http';
import { ErrorHandler, NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';

import * as Raven from 'raven-js';
import { WebsocketService } from '../services/websocket.service';
import { AppComponent } from './app.component';

Raven
  .config('http://3d4bca0e8aa8465bae6fd29934f5ea0f@192.168.64.2:9000/1')
  .install();

export class RavenErrorHandler implements ErrorHandler {
  public handleError(err: any): void {
    Raven.captureException(err);
  }
}

@NgModule({
  bootstrap: [AppComponent],
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
  ],
  providers: [
    WebsocketService,
    { provide: ErrorHandler, useClass: RavenErrorHandler }
  ]
})
export class AppModule { }
