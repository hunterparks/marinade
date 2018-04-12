import { SimulatorComponent } from '../simulator-component.class';

export class Register extends SimulatorComponent {
  public height: number;
  public width: number;
  public x: number;
  public y: number;

  constructor (register: Register) {
    super();
    this.height = register.height;
    this.width = register.width;
    this.x = register.x;
    this.y = register.y;
  }

  public formatTooltip(): string {
    // TODO: populate this
    return '';
  }

  public initialize(): void {
    // TODO: populate this
  }

  public inspect(): void {
    // TODO: populate this
  }
}
