import { Injectable } from '@angular/core';
import { Bus } from '../../../models/simulator/bus/bus.class';
import { ArchitectureService } from '../architecture/architecture.service';

@Injectable()
export class ResponseService {

  constructor (private architectureService: ArchitectureService) { }

  public receiveMessage(message: string): void {
    let messageObject: any = JSON.parse(message);
    Object.keys(messageObject).map((key: string) => {
      let selectedBus: Bus = this.architectureService.architecture.getValue().bus.find((bus: Bus) => {
        return bus.name.toLowerCase() === key;
      });
      if (selectedBus) {
        selectedBus.data.next(messageObject[key].state);
      }
    });
  }

}
