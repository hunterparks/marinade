import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Architecture } from '../../../models/simulator/architecture.class';
import { ARCHITECTURE } from '../../../models/simulator/architecture.model';
import { Bus } from '../../../models/simulator/bus/bus.class';
import { Controller } from '../../../models/simulator/controller/controller.class';
import { Mux } from '../../../models/simulator/mux/mux.class';
import { Register } from '../../../models/simulator/register/register.class';
import { Stage } from '../../../models/simulator/stage/stage.class';
import { RequestService } from '../request/request.service';

@Injectable()
export class ArchitectureService {

  private _architecture: Architecture;
  private readonly componentClasses: { class: any, name: string, services: any[] }[] = [
    { class: Bus,        name: 'bus',           services: [ this.requestService ] },
    { class: Controller, name: 'controller',    services: [ ]                     },
    { class: Mux,        name: 'mux',           services: [ ]                     },
    { class: Stage,      name: 'stage',         services: [ ]                     },
    { class: Register,   name: 'stageRegister', services: [ ]                     },
  ];

  public architecture: BehaviorSubject<Architecture> = new BehaviorSubject<Architecture>(null);

  constructor (private requestService: RequestService) { }

  public load(): void {
    this._architecture = { };
    for (let componentClass of this.componentClasses) {
      // For each object from the architecture configuration
      for (let instance of ARCHITECTURE[componentClass.name]) {
        // If this is the first one, make a place for it in the architecture
        if (!this._architecture[componentClass.name]) {
          this._architecture[componentClass.name] = [ ];
        }
        // Create the class instance using the services and JSON instance
        this._architecture[componentClass.name].push(new componentClass.class(...componentClass.services, instance));
      }
    }
    // Emit the new architecture
    this.architecture.next(this._architecture);
  }

  public unload(): void {
    this._architecture = { };
    this.architecture.next(this._architecture);
  }

}
