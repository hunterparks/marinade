import { Injectable } from '@angular/core';
import { Architecture } from '@models/simulator/architecture.class';
import { ARCHITECTURE } from '@models/simulator/architecture.model';
import { Bus } from '@models/simulator/bus/bus.class';
import { Mux } from '@models/simulator/mux/mux.class';
import { SVGRect } from '@models/simulator/svg/rect.svg.class';
import { RequestService } from '@services/simulator/request/request.service';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

@Injectable()
export class ArchitectureService {

  private _architecture: Architecture;
  private readonly componentClasses: { class: any, name: string, services: any[] }[] = [
    { class: Bus,     name: 'bus',           services: [ this.requestService ] },
    { class: SVGRect, name: 'combinational', services: [ ]                     },
    { class: SVGRect, name: 'controller',    services: [ ]                     },
    { class: Mux,     name: 'mux',           services: [ ]                     },
    { class: SVGRect, name: 'stage',         services: [ ]                     },
    { class: SVGRect, name: 'register',      services: [ ]                     },
  ];

  public architecture: BehaviorSubject<Architecture> = new BehaviorSubject<Architecture>(null);

  constructor(private requestService: RequestService) { }

  public load(): void {
    this._architecture = { };
    for (let componentClass of this.componentClasses) {
      // For each object from the architecture configuration
      for (let instance of ARCHITECTURE[componentClass.name]) {
        // If this is the first one, make a place for it in the architecture
        if (!this._architecture[componentClass.name]) {
          this._architecture[componentClass.name] = [ ];
        }
        if (componentClass.class.name === 'SVGRect') {
          instance.type = componentClass.name;
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
