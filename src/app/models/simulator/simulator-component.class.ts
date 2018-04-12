export abstract class SimulatorComponent {
  public abstract formatTooltip(): string;
  public abstract initialize(): void;
  public abstract inspect(): void;
}
