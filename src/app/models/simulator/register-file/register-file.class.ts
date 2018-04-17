import { SimulatorComponent } from '../simulator-component.class';

export class RegisterFile extends SimulatorComponent {
  public height: number;
  public width: number;
  public x: number;
  public y: number;

  constructor(registerFile: RegisterFile) {
    super();
    this.height = registerFile.height;
    this.width = registerFile.width;
    this.x = registerFile.x;
    this.y = registerFile.y;
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
