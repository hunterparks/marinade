import { Injectable } from '@angular/core';
import { TransmitService } from '../transmit/transmit.service';
import { Bus } from '../../../models/simulator/bus/bus.model';

@Injectable()
export class InspectService {

  constructor(private transmit: TransmitService) { }

  public static formatTooltip(bus: Bus, data?: string): string {
    let tooltipText: string = bus.name + ' (' + bus.width + ')';
    if (data !== undefined) {
      tooltipText += ' - ' + data;
    }
    return tooltipText;
  }

  public inspect(buses: Bus | Bus[]): void {
    if (Array.isArray(buses)) {
      for (let bus of buses) {
        this.transmit.inspect([bus.name.toLowerCase()]);
      }
    } else {
      this.transmit.inspect([buses.name.toLowerCase()]);
    }
  }

}
