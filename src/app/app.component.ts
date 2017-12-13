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
  public count: number = 0;
  public simFlag: boolean = false;

  constructor(private serial: WebsocketService) {
    this.serial.messageSubject.subscribe((result: string) => {
      this.result = result;
      var msg = JSON.parse(result);
      this.count = msg.b1.state;
    });
    this.serial.connect();

    var obj = this
    setInterval(function() {
      if(obj.simFlag){
        obj.step()
      }
    }, 1000)

  }



  public onChange(): void {
    /* tslint:disable-next-line: no-console */ // Todo: Remove this output
    console.log(this.formula);
    this.serial.write(this.formula);
  }

  public simulate(): void {
    this.simFlag = true;
  }

  public step(): void {
    var msg = {
      architecture : {
        simulate : true
      }
    };
    var str = JSON.stringify(msg);
    this.serial.write(str);
  }

  public stop(): void {
    this.simFlag = false;
  }
}
