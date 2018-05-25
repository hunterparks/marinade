import { Injectable } from '@angular/core';
import { Architecture } from '@models/simulator/architecture.class';
import { SVGPath } from '@models/simulator/svg/path.class';
import { SVGRect } from '@models/simulator/svg/rect.class';
import { SVGTrapezoid } from '@models/simulator/svg/trapezoid.class';
import { IpcService } from '@services/ipc/ipc.service';
import { RequestService } from '@services/simulator/request/request.service';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

@Injectable()
export class ArchitectureService {

  private _architecture: Architecture;
  private systemMemory: string;

  public architecture: BehaviorSubject<Architecture> = new BehaviorSubject<Architecture>(null);

  constructor(private requestService: RequestService, private ipcService: IpcService) {
    this.ipcService.on('openFileCallback', (event: Electron.EventEmitter, data: any, filepath: string) => {
      this.parseArchitecture(data);
      this.requestService.load(filepath);
      this.program()
    });
  }

  public program(): void {
    this.requestService.program('./src/backend/assembler/generated_machine_code/machine_code.bin', this.systemMemory);
  }

  private static isEmpty(object: any): boolean {
    return Object.keys(object).length === 0 && object.constructor === Object;
  }

  public load(): void {
    this.ipcService.send('openFile');
  }

  public parseArchitecture(json: any): void {
    this._architecture = { };
    let architecture: any = JSON.parse(json);
    this.systemMemory = architecture['system_memory'];
    this.parseSignals(architecture.signals);
    this.parseEntities(architecture.entities);
    this.architecture.next(this._architecture);
  }

  public parseEntities(entities: any, parent?: any): void {
    if (!this._architecture['rectangle']) {
      this._architecture['rectangle'] = [];
    }
    if (!this._architecture['trapezoid']) {
      this._architecture['trapezoid'] = [];
    }
    for (let entity of entities) {
      if (!ArchitectureService.isEmpty(entity.view) && entity.view.model) {
        if (entity.view.model === 'rectangle') {
          let rectangle: SVGRect = new SVGRect();
          rectangle.parseEntity(entity);
          if (parent) {
            rectangle.setParent(parent);
          }
          this._architecture['rectangle'].push(rectangle);
        } else if (entity.view.model === 'trapezoid') {
          let trapezoid: SVGTrapezoid = new SVGTrapezoid();
          trapezoid.parseEntity(entity);
          this._architecture['trapezoid'].push(trapezoid);
        }
      }
      if (entity.entities) {
        this.parseEntities(entity.entities, entity);
      }
    }
  }

  public parseSignals(signals: any): void {
    if (!this._architecture['path']) {
      this._architecture['path'] = [];
    }
    for (let signal of signals) {
      if (!ArchitectureService.isEmpty(signal.view) && signal.view.model) {
        if (signal.view.model === 'path') {
          let path: SVGPath = new SVGPath(this.requestService);
          path.parseEntity(signal);
          this._architecture['path'].push(path);
        }
      }
    }
  }

  public unload(): void {
    this.requestService.unload();
    this._architecture = null;
    this.architecture.next(this._architecture);
  }

}
