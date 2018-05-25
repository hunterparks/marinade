import { SVGBase } from '@models/simulator/svg/base.interface';

export class SVGRect implements SVGBase{

  public height: number;
  public name?: string;
  public parent?: any;
  public type: string;
  public width: number;
  public x: number;
  public y: number;

  public parseEntity(entity: any): void {
    if (entity.name) {
      this.name = entity.name;
    }
    if (entity.simulation) {
      this.type = entity.simulation.model.toLowerCase();
    } else {
      this.type = 'stage';
    }
    this.height = entity.view.height;
    this.width = entity.view.width;
    this.x = entity.view.x;
    this.y = entity.view.y;
  }

  public setParent(parent: any): void {
    this.parent = parent;
  }

}
