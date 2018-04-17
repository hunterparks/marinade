import { SimulatorComponent } from '../simulator-component.class';

export class Stage extends SimulatorComponent {
  public height: number;
  public width: number;
  public x: number;
  public y: number;

  constructor(stage: Stage) {
    super();
    this.height = stage.height;
    this.width = stage.width;
    this.x = stage.x;
    this.y = stage.y;
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
