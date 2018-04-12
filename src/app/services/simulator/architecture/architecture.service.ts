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

  private _architecture: Architecture = null;
  public architecture: BehaviorSubject<Architecture> = new BehaviorSubject<Architecture>(null);

  constructor (private requestService: RequestService) { }

  public load(): void {
    this._architecture = { bus: [], controller: [], mux: [], stage: [], stageRegister: [] };
    for (let bus of ARCHITECTURE.bus) {
      this._architecture.bus.push(new Bus(this.requestService, bus));
    }
    for (let controller of ARCHITECTURE.controller) {
      this._architecture.controller.push(new Controller(controller));
    }
    for (let mux of ARCHITECTURE.mux) {
      this._architecture.mux.push(new Mux(mux));
    }
    for (let stage of ARCHITECTURE.stage) {
      this._architecture.stage.push(new Stage(stage));
    }
    for (let stageRegister of ARCHITECTURE.stageRegister) {
      this._architecture.stageRegister.push(new Register(stageRegister));
    }
    this.architecture.next(this._architecture);
  }

  public unload(): void {
    this._architecture = null;
    this.architecture.next(this._architecture);
  }

}
