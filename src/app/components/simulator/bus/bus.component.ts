import { Component, HostListener, Input, OnInit } from '@angular/core';

@Component({
  selector: '[svg-bus]',
  styleUrls: ['./bus.component.sass'],
  templateUrl: './bus.component.html',
})
export class BusComponent implements OnInit {

  // The default bus color (without highlight)
  private static DEFAULT_COLOR: string = '#000000';
  // The highlighted bus color (when moused over)
  private static HIGHLIGHT_COLOR: string = '#ff0000';
  // The clicked bus color
  private static SELECT_COLOR: string = '#00ff00';

  // The svg paths for the arrow heads
  public arrows: string[] = [];
  // Input string with a list of coordinates
  @Input('svg-bus') public bus: { 'data': string, 'junction'?: number, 'name': string, 'paths': string[] } = null;
  // The active color of the bus
  public color: string = BusComponent.DEFAULT_COLOR;
  // The junction point for a complex bus
  public junctions: any[] = [];
  // Text associated with bus
  public name: string = '';
  // Generated svg paths for the bus
  public paths: string[] = [];

  /**
   * Determines the direction of the arrows using the last two points of the path
   * @param {number[]} secondLastPoint The second to last point in the path
   * @param {number[]} lastPoint The last point in the path
   * @returns {string} The direction to draw the arrows in - 'up', 'down', 'left', or 'right'
   */
  private static arrowDirection(secondLastPoint: number[], lastPoint: number[]): string {
    let direction: string = '';
    // Line is moving to the right
    if (lastPoint[0] > secondLastPoint[0]) {
      direction = 'right';
    // Line is moving to the left
    } else if (lastPoint[0] < secondLastPoint[0]) {
      direction = 'left';
    // Line is moving down
    } else if (lastPoint[1] > secondLastPoint[1]) {
      direction = 'down';
    // Line is moving up
    } else if (lastPoint[1] < secondLastPoint[1]) {
      direction = 'up';
    }
    return direction;
  }

  /**
   * Draws the arrow head centered on a point using a given direction
   * @param {number} pointX The x coordinate of the center point
   * @param {number} pointY The y coordinate of the center point
   * @param {string} direction The direction the arrow head is pointing
   * @param {number} size The size of the arrow head
   */
  private drawArrow(pointX: number, pointY: number, direction: string, size: number = 5): void {
    this.arrows.push('');
    // Set up placeholder variables
    let deltaY: number = size;
    let deltaX: number = size;
    let vertical: boolean = false;
    // Change drawing behavior based on the direction
    switch (direction) {
      case 'up': vertical = true; deltaY = -deltaY; break;
      case 'down': vertical = true; break;
      case 'left': deltaX = -deltaX; break;
      case 'right': break;
    }
    // Append to the arrow
    if (vertical) {
      this.arrows[this.arrows.length - 1] += ' M ' + pointX + ' ' + pointY;
      this.arrows[this.arrows.length - 1] += ' L ' + (pointX + deltaX) + ' ' + pointY;
      this.arrows[this.arrows.length - 1] += ' L ' + pointX + ' ' + (pointY + deltaY);
      this.arrows[this.arrows.length - 1] += ' L ' + (pointX - deltaX) + ' ' + pointY;
    } else {
      this.arrows[this.arrows.length - 1] += ' M ' + pointX + ' ' + pointY;
      this.arrows[this.arrows.length - 1] += ' L ' + pointX + ' ' + (pointY + deltaY);
      this.arrows[this.arrows.length - 1] += ' L ' + (pointX + deltaX) + ' ' + pointY;
      this.arrows[this.arrows.length - 1] += ' L ' + pointX + ' ' + (pointY - deltaY);
    }
    // Return to the starting point
    this.arrows[this.arrows.length - 1] += ' Z';
  }

  /**
   * Draws the path that creates the line for the bus, with the arrow at the end
   * @param {number[][]} coordinates A list of x, y coordinates that create the line for the bus
   */
  private drawBus(coordinates: number[][]): void {
    // Reset the paths bus
    this.paths.push('');
    // Iterate through the coordinates and build the paths bus
    for (let i: number = 0; i < coordinates.length; i++) {
      if (i === 0) {
        this.paths[this.paths.length - 1] += 'M ';
      } else {
        this.paths[this.paths.length - 1]  += ' L ';
      }
      this.paths[this.paths.length - 1]  += coordinates[i][0] + ' ' + coordinates[i][1];
    }
    // Draw the arrows using the last two points in the bus
    this.drawArrow(
      coordinates[coordinates.length - 1][0],
      coordinates[coordinates.length - 1][1],
      BusComponent.arrowDirection(coordinates[coordinates.length - 2], coordinates[coordinates.length - 1])
    );
  }

  /**
   * Parses the points on the line that create the bus
   * @returns {number[][]} A list of x, y coordinates that create the line for the bus
   */
  private parsePoints(path: string): number[][] {
    // Create the coordinates array
    let coordinates: number[][] = [];
    // Split on commas to separate pairs of x, y coordinates
    path.split(',').forEach((line: string) => {
      // Split each set of points on the space, and parse as numbers
      coordinates.push(line.trim().split(' ').map(Number));
    });
    return coordinates;
  }

  /**
   * Read the input object and draw the bus
   */
  public ngOnInit(): void {
    for (let path of this.bus['paths']) {
      let coordinates: number[][] = this.parsePoints(path);
      this.drawBus(coordinates);
    }
    if (this.bus['junctions']) {
      this.junctions = this.bus['junctions'];
    }
    if (this.bus['name']) {
      this.name = this.bus['name'];
    }
  }

  /**
   * Handles the mouseClick event
   */
  @HostListener('click')
  public onClick(): void {
    // Change the bus color to the select color
    this.color = BusComponent.SELECT_COLOR;
    // Expand hovering tooltip
  }

  /**
   * Handles the mouseEnter event
   */
  @HostListener('mouseenter')
  public onMouseEnter(): void {
    // Change the bus color to the highlight color
    this.color = BusComponent.HIGHLIGHT_COLOR;
    // Spawn hovering tooltip
  }

  /**
   * Handles the mouseLeave event
   */
  @HostListener('mouseleave')
  public onMouseLeave(): void {
    // Change the bus color to the default color
    this.color = BusComponent.DEFAULT_COLOR;
  }

}
