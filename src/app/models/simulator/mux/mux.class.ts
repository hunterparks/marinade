import { SimulatorComponent } from '../simulator-component.class';

export class Mux extends SimulatorComponent {
  public path: string;

  constructor(mux: Mux) {
    super();
    this.path = mux.path;
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
