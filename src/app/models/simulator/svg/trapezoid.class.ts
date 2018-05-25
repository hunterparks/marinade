import { SVGBase } from '@models/simulator/svg/base.interface';

export class SVGTrapezoid implements SVGBase {

  public inputs: number;
  public outputs: number;
  public notched: boolean = false;
  public x: number;
  public y: number;

  public parseEntity(entity: any): void {
    if (entity.view.notched) {
      this.notched = entity.view.notched;
    }
    this.inputs = entity.simulation.inputs.length;
    this.outputs = 1;
    this.x = entity.view.x;
    this.y = entity.view.y;
  }

}
