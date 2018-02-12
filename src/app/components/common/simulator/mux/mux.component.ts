import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: '[svg-mux]',
  styleUrls: ['./mux.component.sass'],
  templateUrl: './mux.component.html',
})
export class MuxComponent implements OnInit{

  public color: string = '';
  @Input('svg-mux') public mux: any = null;
  public svg: string = '';

  private drawMux(coordinates: number[][]): void {
    // Reset the paths bus
    this.svg = '';
    // Iterate through the coordinates and build the paths bus
    for (let i: number = 0; i < coordinates.length; i++) {
      if (i === 0) {
        this.svg += 'M ';
      } else {
        this.svg += ' L ';
      }
      this.svg += coordinates[i][0] + ' ' + coordinates[i][1];
    }
    this.svg += ' Z';
  }

  private parsePoints(): number[][] {
    // Create the coordinates array
    let coordinates: number[][] = [];
    // Split on commas to separate pairs of x, y coordinates
    this.mux['path'].split(',').forEach((line: string) => {
      // Split each set of points on a space, and parse as numbers
      coordinates.push(line.trim().split(' ').map(Number));
    });
    return this.rotateCW(coordinates);
  }

  /**
   * Rotate the mux 90 clockwise - required since draw.io does a rotation on them
   * @param {number[][]} coordinates The original coordinate array
   * @returns {number[][]} The rotated coordinate array
   */
  private rotateCW(coordinates: number[][]): number[][] {
    // Find the mux bounds
    let minX: number = Number.MAX_VALUE;
    let maxX: number = Number.MIN_VALUE;
    let minY: number = Number.MAX_VALUE;
    let maxY: number = Number.MIN_VALUE;
    coordinates.forEach((coordinate: number[]) => {
      if (coordinate[0] < minX) {
        minX = coordinate[0];
      }
      if (coordinate[1] < minY) {
        minY = coordinate[1];
      }
      if (coordinate[0] > maxX) {
        maxX = coordinate[0];
      }
       if (coordinate[1] > maxY) {
        maxY = coordinate[1];
       }
    });
    // Find the mux center - this is the point the mux is rotated around
    let centerX: number = (minX + maxX) / 2;
    let centerY: number = (minY + maxY) / 2;
    // Adjust the coordinates
    coordinates.forEach((coordinate: number[]) => {
      coordinate[0] -= centerX;
      coordinate[1] -= centerY;
      let temp: number = coordinate[0];
      coordinate[0] = -coordinate[1];
      coordinate[1] = temp;
      coordinate[0] += centerX;
      coordinate[1] += centerY;
    });
    return coordinates;
  }

  public ngOnInit(): void {
    this.color = this.mux['color'];
    this.drawMux(this.parsePoints());
  }
}
