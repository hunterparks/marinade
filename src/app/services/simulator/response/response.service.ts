import { Injectable } from '@angular/core';
import { SVGPath } from '@models/simulator/svg/path.class';
import { ArchitectureService } from '@services/simulator/architecture/architecture.service';

@Injectable()
export class ResponseService {

  constructor(private architectureService: ArchitectureService) { }

  public receiveMessage(message: string): void {
    let messageObject: any = JSON.parse(message);
    Object.keys(messageObject).map((key: string) => {
      let architecture: any = this.architectureService.architecture.getValue();
      if (architecture) {
        let selectedBus: SVGPath = this.architectureService.architecture.getValue().path.find((path: SVGPath) => {
          return path.name.toLowerCase() === key;
        });
        if (selectedBus) {
          selectedBus.data.next(messageObject[key].state);
        }
      }
    });

  }

}
