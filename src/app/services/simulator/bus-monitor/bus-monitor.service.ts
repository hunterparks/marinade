import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Bus } from '../../../models/simulator/bus/bus.class';

@Injectable()
export class BusMonitorService {

  public buses: BehaviorSubject<Bus[]> = new BehaviorSubject<Bus[]>([]);

  private findBus(search: Bus): number {
    return this.buses.getValue().findIndex((bus: Bus) => {
      return bus.equals(search);
    });
  }

  public addBus(bus: Bus): boolean {
    if (this.findBus(bus) === -1) {
      this.buses.getValue().push(bus);
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

}
