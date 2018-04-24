import { SimulatorComponent } from '../simulator-component.class';

export class Controller extends SimulatorComponent {
  public height: number;
  public width: number;
  public x: number;
  public y: number;

  constructor(controller: Controller) {
    super();
    this.height = controller.height;
    this.width = controller.width;
    this.x = controller.x;
    this.y = controller.y;
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
