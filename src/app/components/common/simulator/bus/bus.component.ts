import { Component, Input, OnInit } from '@angular/core';

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

  // The active color of the bus
  public color: string = BusComponent.DEFAULT_COLOR;
  // Input string with a list of coordinates
  @Input('svg-bus') public path: string = '';
  // Generated svg path
  public svg: string = '';

  /**
   * Determines the direction of the arrow using the last two points of the path
   * @param {number[]} secondLastPoint The second to last point in the path
   * @param {number[]} lastPoint The last point in the path
   * @returns {string} The direction to draw the arrow in - 'up', 'down', 'left', or 'right'
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
  private drawArrow(pointX: number, pointY: number, direction: string, size: number = 4): void {
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
    // Append to the svg
    if (vertical) {
      this.svg += ' M ' + pointX + ' ' + pointY;
      this.svg += ' L ' + (pointX + deltaX) + ' ' + pointY;
      this.svg += ' L ' + pointX + ' ' + (pointY + deltaY);
      this.svg += ' L ' + (pointX - deltaX) + ' ' + pointY;
      this.svg += ' L ' + pointX + ' ' + pointY;
    } else {
      this.svg += ' M ' + pointX + ' ' + pointY;
      this.svg += ' L ' + pointX + ' ' + (pointY + deltaY);
      this.svg += ' L ' + (pointX + deltaX) + ' ' + pointY;
      this.svg += ' L ' + pointX + ' ' + (pointY - deltaY);
      this.svg += ' L ' + pointX + ' ' + pointY;
    }
  }

  /**
   * Draws the path that creates the line for the bus, with the arrow at the end
   * @param {number[][]} coordinates A list of x, y coordinates that create the line for the bus
   */
  private drawBus(coordinates: number[][]): void {
    // Reset the svg path
    this.svg = '';
    // Iterate through the coordinates and build the svg path
    for (let i: number = 0; i < coordinates.length; i++) {
      if (i === 0) {
        this.svg += 'M ';
      } else {
        this.svg += ' L ';
      }
      this.svg += coordinates[i][0] + ' ' + coordinates[i][1];
    }
    // Draw the arrow using the last two points in the path
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
  private parsePoints(): number[][] {
    // Create the coordinates array
    let coordinates: number[][] = [];
    // Split on commas to separate pairs of x, y coordinates
    this.path.split(',').forEach((line: string) => {
      // Split each set of points on the space, and parse as numbers
      coordinates.push(line.trim().split(' ').map(Number));
    });
    return coordinates;
  }

  /**
   * Read the input path and draw the bus
   */
  public ngOnInit(): void {
    let coordinates: number[][] = this.parsePoints();
    this.drawBus(coordinates);
  }

  /**
   * Handles the mouseEnter event
   */
  public onEnter(): void {
    // Change the bus color to the highlight color
    this.color = BusComponent.HIGHLIGHT_COLOR;
  }

  /**
   * Handles the mouseLeave event
   */
  public onLeave(): void {
    // Change the bus color to the default color
    this.color = BusComponent.DEFAULT_COLOR;
  }

}
