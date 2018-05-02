export class SVGRect {

  public height: number;
  public name?: string;
  public type: string;
  public width: number;
  public x: number;
  public y: number;

  constructor(block: SVGRect) {
    this.height = block.height;
    if (block.name) {
      this.name = block.name;
    }
    this.type = block.type;
    this.width = block.width;
    this.x = block.x;
    this.y = block.y;
  }

}
