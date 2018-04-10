import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { ARCHITECTURE } from '../../../models/simulator/architecture.model';
import { Simulator } from '../../../models/simulator/simulator.model';
import { InspectService } from '../inspect/inspect.service';

@Injectable()
export class MonitorService {

  public architecture: Simulator = null;

  public loadArchitecture(): BehaviorSubject<Simulator> {
    this.architecture = ARCHITECTURE;
    for (let bus of this.architecture.bus) {
      bus.data = new BehaviorSubject<string>(InspectService.formatTooltip(bus));
      bus.state = new BehaviorSubject<string>('inactive');
    }
    return new BehaviorSubject<Simulator>(this.architecture);
  }

}
