import { Component } from '@angular/core';
import {
  ARCHITECTURE1, ARCHITECTURE2, ARCHITECTURE3, ARCHITECTURE4, ARCHITECTURE5, ARCHITECTURE6, ARCHITECTURE7,
  ARCHITECTURE8, ARCHITECTURE9
} from './simulator.model';

@Component({
  selector: 'marinade-simulator',
  styleUrls: ['./simulator.component.sass'],
  templateUrl: './simulator.component.html',
})
export class SimulatorComponent {

  private mouseStartX: number = -1;
  private mouseStartY: number = -1;
  private tracking: boolean = false;
  private viewBoxHeight: number = 905;
  private viewBoxUpperLeftX: number = 0;
  private viewBoxUpperLeftY: number = 0;
  private viewBoxWidth: number = 1600;

  public architecture: string = ARCHITECTURE1 + ARCHITECTURE2 + ARCHITECTURE3 + ARCHITECTURE4 + ARCHITECTURE5 +
                                ARCHITECTURE6 + ARCHITECTURE7 + ARCHITECTURE8 + ARCHITECTURE9;
  public scale: number = 1;
  public viewBox: string = '0 0 1600 905';

  private updateViewBox(): string {
    if (this.viewBoxUpperLeftX < -1400) {
      this.viewBoxUpperLeftX = -1400;
    }
    if (this.viewBoxUpperLeftX > 1400) {
      this.viewBoxUpperLeftX = 1400;
    }
    if (this.viewBoxUpperLeftY < -700) {
      this.viewBoxUpperLeftY = -700;
    }
    if (this.viewBoxUpperLeftY > 800) {
      this.viewBoxUpperLeftY = 800;
    }
    this.viewBox = this.viewBoxUpperLeftX + ' ' + this.viewBoxUpperLeftY + ' ' +
      this.viewBoxWidth / this.scale + ' ' + this.viewBoxHeight / this.scale;
    return this.viewBox;
  }

  public onClick(event: MouseEvent): void {
    this.mouseStartX = event.x;
    this.mouseStartY = event.y;
    this.tracking = true;
  }

  public onMove(event: MouseEvent): void {
    if (this.tracking) {
      this.viewBoxUpperLeftX = this.viewBoxUpperLeftX - (event.x - this.mouseStartX) / this.scale;
      this.viewBoxUpperLeftY = this.viewBoxUpperLeftY - (event.y - this.mouseStartY) / this.scale;
      this.updateViewBox();
      this.mouseStartX = event.x;
      this.mouseStartY = event.y;
    }
  }

  public onRelease(): void {
    this.mouseStartX = 0;
    this.mouseStartY = 0;
    this.tracking = false;
  }

  public onWheel(event: WheelEvent): void {
    let oldScale: number = this.scale;
    this.scale += event.deltaY / 400;
    if (this.scale < 0.6) {
      this.scale = 0.6;
    }
    if (this.scale > 2.0) {
      this.scale = 2.0;
    }
    let deltaX: number = (event.layerX - this.viewBoxUpperLeftX) * (this.scale - oldScale);
    let deltaY: number = (event.layerY - this.viewBoxUpperLeftY) * (this.scale - oldScale);
    this.viewBoxUpperLeftX += deltaX;
    this.viewBoxUpperLeftY += deltaY;
    this.updateViewBox();
  }

  public reset(): void {
    this.viewBox = '0 0 1600 905';
    this.scale = 1;
  }

}
