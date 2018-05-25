import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: '[svg-trapezoid]',
  styleUrls: ['./trapezoid.component.sass'],
  templateUrl: './trapezoid.component.html',
})
export class TrapezoidComponent implements OnInit {

  public static HEIGHT: number = 100;
  public static WIDTH: number = 40;

  public svg: string = '';
  @Input('svg-trapezoid') public trapezoid: any = null;

  private drawMux(): void {
    this.svg =   'M ' + (this.trapezoid.x - TrapezoidComponent.WIDTH / 2) + ' ' + (this.trapezoid.y - TrapezoidComponent.HEIGHT / 2);
    if (this.trapezoid.notched) {
      this.svg += ' L ' + (this.trapezoid.x - TrapezoidComponent.WIDTH / 2) + ' ' + (this.trapezoid.y - TrapezoidComponent.HEIGHT / 6);
      this.svg += ' L ' + (this.trapezoid.x - TrapezoidComponent.WIDTH / 4) + ' ' + (this.trapezoid.y);
      this.svg += ' L ' + (this.trapezoid.x - TrapezoidComponent.WIDTH / 2) + ' ' + (this.trapezoid.y + TrapezoidComponent.HEIGHT / 6);
    }
    this.svg += ' L ' + (this.trapezoid.x - TrapezoidComponent.WIDTH / 2) + ' ' + (this.trapezoid.y + TrapezoidComponent.HEIGHT / 2);
    this.svg += ' L ' + (this.trapezoid.x + TrapezoidComponent.WIDTH / 2) + ' ' + (this.trapezoid.y + TrapezoidComponent.HEIGHT / 2 - 20);
    this.svg += ' L ' + (this.trapezoid.x + TrapezoidComponent.WIDTH / 2) + ' ' + (this.trapezoid.y - TrapezoidComponent.HEIGHT / 2 + 20);
    this.svg += ' Z';
  }

  public ngOnInit(): void {
    this.drawMux();
  }
}
