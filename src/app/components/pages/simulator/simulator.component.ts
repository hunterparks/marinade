import { Component, Host, HostListener } from '@angular/core';
import { TooltipService } from '../../../services/tooltip/tooltip.service';
import { BUSES } from '../../common/simulator/bus/buses.model';
import { LABELS } from '../../common/simulator/label/labels.model';
import { MUXES } from '../../common/simulator/mux/muxes.model';
import { REGISTERS } from '../../common/simulator/register/registers.model';

@Component({
  selector: 'marinade-simulator',
  styleUrls: ['./simulator.component.sass'],
  templateUrl: './simulator.component.html',
})
export class SimulatorComponent {

  private static readonly DEFAULT_VIEWBOX_HEIGHT: number = 900;
  private static readonly DEFAULT_VIEWBOX_SCALE: number = 1;
  private static readonly DEFAULT_VIEWBOX_UPPER_LEFT_X: number = 0;
  private static readonly DEFAULT_VIEWBOX_UPPER_LEFT_Y: number = 0;
  private static readonly DEFAULT_VIEWBOX_WIDTH: number = 1600;

  private static readonly MAX_SCALE: number = 2.5;
  private static readonly MIN_SCALE: number = 1.0;

  private mouseStartX: number = -1;
  private mouseStartY: number = -1;
  private tracking: boolean = false;
  private viewBoxHeight: number = 900;
  private viewBoxUpperLeftX: number = 0;
  private viewBoxUpperLeftY: number = 0;
  private viewBoxWidth: number = 1600;

  public buses: any[] = BUSES;
  public labels: any[] = LABELS;
  public muxes: any[] = MUXES;
  public registers: any[] = REGISTERS;

  public scale: number = 1;
  public viewBox: string = '0 0 1600 900';

  constructor(private tooltipService: TooltipService) {}

  private updateViewBox(): void {
    // Bound the architecture on the left
    if (this.viewBoxUpperLeftX < -this.viewBoxWidth * 0.5) {
      this.viewBoxUpperLeftX = -this.viewBoxWidth * 0.5;
    }
    // Bound the architecture on the right
    if (this.viewBoxUpperLeftX / this.scale > this.viewBoxWidth) {
      this.viewBoxUpperLeftX = this.viewBoxWidth * (this.scale - SimulatorComponent.MAX_SCALE);
    }
    // Bound the architecture on the top
    if (this.viewBoxUpperLeftY < -this.viewBoxHeight * 0.5) {
      this.viewBoxUpperLeftY = -this.viewBoxHeight * 0.5;
    }
    // Bound the architecture on the bottom
    if (this.viewBoxUpperLeftY / this.scale > this.viewBoxHeight) {
      this.viewBoxUpperLeftY = this.viewBoxHeight * (this.scale - SimulatorComponent.MAX_SCALE);
    }
    this.viewBox = this.viewBoxUpperLeftX + ' ' + this.viewBoxUpperLeftY + ' ' +
                   this.viewBoxWidth + ' ' + this.viewBoxHeight;
  }

  /**
   * Start tracking the mouse drag motion
   * @param {MouseEvent} event The MouseEvent that caused the click function to fire
   */
  @HostListener('mousedown', ['$event'])
  public onClick(event: MouseEvent): void {
    // Note the original location of the cursor
    this.mouseStartX = event.x;
    this.mouseStartY = event.y;
    // Allow movements to move the canvas
    this.tracking = true;
  }

  /**
   * Pan the canvas based on the direction of the cursor movements
   * @param {MouseEvent} event The MouseEvent that caused the move function to fire
   */
  @HostListener('mousemove', ['$event'])
  public onMove(event: MouseEvent): void {
    // If a click is being held
    if (this.tracking) {
      this.tooltipService.tooltips.forEach((tooltip: any) => {
        tooltip.x.next(tooltip.x.getValue() + (event.x - this.mouseStartX) / this.scale);
        tooltip.y.next(tooltip.y.getValue() + (event.y - this.mouseStartY) / this.scale);
      });
      // Adjust the top left corner (origin point) based on the location deltas and the scale
      this.viewBoxUpperLeftX = this.viewBoxUpperLeftX - (event.x - this.mouseStartX) / this.scale;
      this.viewBoxUpperLeftY = this.viewBoxUpperLeftY - (event.y - this.mouseStartY) / this.scale;
      // Refresh the viewbox with the new properties
      this.updateViewBox();
      // Create a new reference point for tracking
      this.mouseStartX = event.x;
      this.mouseStartY = event.y;
    }
  }

  /**
   * Stop tracking the mouse drag motion
   */
  @HostListener('mouseup')
  public onRelease(): void {
    // Reset the mouse tracking locations
    this.mouseStartX = 0;
    this.mouseStartY = 0;
    // Prevent movements from moving the canvas
    this.tracking = false;
  }

  /**
   * Scales the viewbox using the mousewheel
   * @param {WheelEvent} event The mousewheel event that called this function
   */
  @HostListener('wheel', ['$event'])
  public onWheel(event: WheelEvent): void {
    // TODO scaling for tooltips
    // Adjust the scale
    this.scale += event.deltaY / 400;
    if (this.scale < SimulatorComponent.MIN_SCALE) {
      this.scale = SimulatorComponent.MIN_SCALE;
    }
    if (this.scale > SimulatorComponent.MAX_SCALE) {
      this.scale = SimulatorComponent.MAX_SCALE;
    }
    // Find the old center
    let oldCenterX: number = this.viewBoxWidth / 2;
    let oldCenterY: number = this.viewBoxHeight / 2;
    // Adjust the current height
    this.viewBoxHeight = SimulatorComponent.DEFAULT_VIEWBOX_HEIGHT / this.scale;
    this.viewBoxWidth = SimulatorComponent.DEFAULT_VIEWBOX_WIDTH / this.scale;
    // Find the new center
    let centerX: number = this.viewBoxWidth / 2;
    let centerY: number = this.viewBoxHeight / 2;
    // Pan the view so it zooms on the center
    this.viewBoxUpperLeftX += oldCenterX - centerX;
    this.viewBoxUpperLeftY += oldCenterY - centerY;
    this.updateViewBox();
  }

  /**
   * Reset the viewBox to the default view (scale 1.0; top-left corner at 0, 0)
   */
  public reset(): void {
    // Reset the height and width properties to remove any zooming
    this.viewBoxHeight = SimulatorComponent.DEFAULT_VIEWBOX_HEIGHT;
    this.viewBoxWidth = SimulatorComponent.DEFAULT_VIEWBOX_WIDTH;
    // Reset the upper left corner to remove any panning
    this.viewBoxUpperLeftX = SimulatorComponent.DEFAULT_VIEWBOX_UPPER_LEFT_X;
    this.viewBoxUpperLeftY = SimulatorComponent.DEFAULT_VIEWBOX_UPPER_LEFT_Y;
    // Reset the scale used for calculations
    this.scale = SimulatorComponent.DEFAULT_VIEWBOX_SCALE;
    // Refresh the viewBox with the new properties
    this.updateViewBox();
  }

}
