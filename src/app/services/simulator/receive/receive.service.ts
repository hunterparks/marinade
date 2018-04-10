import { Injectable } from '@angular/core';
import { Bus } from '../../../models/simulator/bus/bus.model';
import { InspectService } from '../inspect/inspect.service';
import { MonitorService } from '../monitor/monitor.service';

@Injectable()
export class ReceiveService {

  constructor(private monitor: MonitorService) { }

  public receiveMessage(message: string): void {
    let messageObject: any = JSON.parse(message);
    Object.keys(messageObject).map((key: string) => {
      let selectedBus: Bus = this.monitor.architecture.bus.find((bus: Bus) => {
        return bus.name.toLowerCase() === key;
      });
      if (selectedBus) {
        selectedBus.data.next(InspectService.formatTooltip(selectedBus, messageObject[key].state));
      }
    });
  }

}
