import { Component } from '@angular/core';

import { WebsocketService } from '../services/websocket.service';

@Component({
  selector: 'marinade-root',
  styleUrls: ['./app.component.css'],
  templateUrl: './app.component.html',
})
export class AppComponent {
  public formula: string = '1 + 1';
  public result: string = '';

  constructor(private serial: WebsocketService) {
    this.serial.messageSubject.subscribe((result: string) => {
      this.result = result;
    });
    this.serial.connect();
  }

  public onChange(): void {
    /* tslint:disable-next-line: no-console */ // Todo: Remove this output
    console.log(this.formula);
    this.serial.write(this.formula);
  }
}
