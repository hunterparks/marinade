import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { ARCHITECTURE } from '../../../models/simulator/architecture.model';
import { Simulator } from '../../../models/simulator/simulator.model';
import { InspectService } from '../inspect/inspect.service';

@Injectable()
export class ArchitectureService {

  private _architecture: Simulator = null;
  public architecture: BehaviorSubject<Simulator> = new BehaviorSubject<Simulator>(null);

  private initializeBuses(): void {
    for (let bus of this._architecture.bus) {
      bus.data = new BehaviorSubject<string>(InspectService.formatTooltip(bus));
      bus.state = new BehaviorSubject<string>('inactive');
    }
  }

  public load(): void {
    this._architecture = ARCHITECTURE;
    this.initializeBuses();
    this.architecture.next(this._architecture);
  }

  public unload(): void {
    this._architecture = null;
    this.architecture.next(this._architecture);
  }

}
