import { Injectable } from '@angular/core';
import { SVGPath } from '@models/simulator/svg/path.class';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

@Injectable()
export class BusMonitorService {

  public paths: BehaviorSubject<SVGPath[]> = new BehaviorSubject<SVGPath[]>([]);

  private findBus(search: SVGPath): number {
    return this.paths.getValue().findIndex((path: SVGPath) => {
      return path.equals(search);
    });
  }

  public addBus(path: SVGPath): boolean {
    if (this.findBus(path) === -1) {
      this.paths.getValue().push(path);
      return true;
    }
    return false;
  }

  public deleteBus(path: SVGPath): boolean {
    let index: number = this.findBus(path);
    if (index !== -1) {
      this.paths.getValue().splice(index, 1);
      return true;
    }
    return false;
  }

}
