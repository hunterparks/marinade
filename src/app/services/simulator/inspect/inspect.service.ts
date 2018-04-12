import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Bus } from '../../../models/simulator/bus/bus.model';
import { RequestService } from '../request/request.service';

@Injectable()
export class InspectService {

  public buses: BehaviorSubject<Bus[]> = new BehaviorSubject<Bus[]>([]);

  constructor (private requestService: RequestService) { }

  private static compareBuses(busA: Bus, busB: Bus): number {
    if (busA.name < busB.name) {
      return -1;
    }
    if (busA.name > busB.name) {
      return 1;
    }
    return 0;
  }

  public static formatTooltip(bus: Bus, data?: string): string {
    let tooltipText: string = bus.name + ' (' + bus.width + ')';
    if (data !== undefined) {
      tooltipText += ' - ' + data;
    }
    return tooltipText;
  }

  private findBus(search: Bus): number {
    return this.buses.getValue().findIndex((bus: Bus) => {
      return bus.name === search.name;
    });
  }

  public addBus(bus: Bus): boolean {
    if (this.findBus(bus) === -1) {
      this.buses.getValue().push(bus);
      this.buses.getValue().sort(InspectService.compareBuses);
      return true;
    }
    return false;
  }

  public deleteBus(bus: Bus): boolean {
    let index: number = this.findBus(bus);
    if (index !== -1) {
      this.buses.getValue().splice(index, 1);
      return true;
    }
    return false;
  }

  public getBuses(): Bus[] {
    return this.buses.getValue();
  }

  public inspect(buses: Bus | Bus[]): void {
    if (Array.isArray(buses)) {
      for (let bus of buses) {
        this.requestService.inspect([bus.name.toLowerCase()]);
      }
    } else {
      this.requestService.inspect([buses.name.toLowerCase()]);
    }
  }

}
