import { SimulatorComponent } from '../simulator-component.class';

export class Combinational extends SimulatorComponent {
  public height: number;
  public name: string;
  public width: number;
  public x: number;
  public y: number;

  constructor(combinational: Combinational) {
    super();
    this.height = combinational.height;
    this.name = combinational.name;
    this.width = combinational.width;
    this.x = combinational.x;
    this.y = combinational.y;
  }

  public initialize(): void {
    // TODO: populate this
  }

  public inspect(): void {
    // TODO: populate this
  }

}
