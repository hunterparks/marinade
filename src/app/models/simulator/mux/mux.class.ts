export class Mux {
  public inputs: number;
  public outputs: number;
  public x: number;
  public y: number;

  constructor(mux: Mux) {
    this.inputs = mux.inputs;
    this.outputs = mux.outputs;
    this.x = mux.x;
    this.y = mux.y;
  }
}
