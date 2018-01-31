import { Component } from '@angular/core';
import {ARCHITECTURE, ARCHITECTURE2} from './simulator.model';

@Component({
  selector: 'marinade-simulator',
  styleUrls: ['./simulator.component.sass'],
  templateUrl: './simulator.component.html',
})
export class SimulatorComponent {

  private mouseStartX: number = -1;
  private mouseStartY: number = -1;
  private tracking: boolean = false;
  public architecture: string = ARCHITECTURE + ARCHITECTURE2;
  public viewBoxUpperLeftX: number = 0;
  public viewBoxUpperLeftY: number = 0;

  public onClick(event: MouseEvent): void {
    this.mouseStartX = event.x;
    this.mouseStartY = event.y;
    this.tracking = true;
  }

  public onMove(event: MouseEvent): void {
    if (this.tracking) {
      this.viewBoxUpperLeftX = event.x - this.mouseStartX;
      this.viewBoxUpperLeftY = event.y - this.mouseStartY;
    }
  }

  public onRelease(event: MouseEvent): void {
    this.mouseStartX = -1;
    this.mouseStartY = -1;
    this.tracking = false;
  }

}
