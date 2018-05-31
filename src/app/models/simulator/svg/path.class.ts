import { Inject } from '@angular/core';
import { SVGBase } from '@models/simulator/svg/base.interface';
import { RequestService } from '@services/simulator/request/request.service';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

export enum PathState {
  Active,
  Inactive
}

export class SVGPath implements SVGBase {

  public arrows: string[] = [];
  public data?: BehaviorSubject<string>;
  public junctions: number[][];
  public name: string;
  public segments: string[];
  public state?: BehaviorSubject<PathState>;
  public tooltip: BehaviorSubject<string>;
  public width: number;

  constructor(@Inject(RequestService) private requestService?: RequestService) { }

  private static arrowDirection(secondLastPoint: number[], lastPoint: number[]): string {
    let direction: string = '';
    if (lastPoint[0] > secondLastPoint[0]) {
      direction = 'right';
    } else if (lastPoint[0] < secondLastPoint[0]) {
      direction = 'left';
    } else if (lastPoint[1] > secondLastPoint[1]) {
      direction = 'down';
    } else if (lastPoint[1] < secondLastPoint[1]) {
      direction = 'up';
    }
    return direction;
  }

  private drawArrow(pointX: number, pointY: number, direction: string, size: number = 5): void {
    this.arrows.push('');
    let deltaY: number = size;
    let deltaX: number = size;
    let vertical: boolean = false;
    switch (direction) {
      case 'up': vertical = true; deltaY = -deltaY; break;
      case 'down': vertical = true; break;
      case 'left': deltaX = -deltaX; break;
      case 'right': break;
    }
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
    this.arrows[this.arrows.length - 1] += ' Z';
  }

  private drawBus(coordinates: number[][]): void {
    if (coordinates.length > 0) {
      this.segments.push('');
      for (let i: number = 0; i < coordinates.length; i++) {
        if (i === 0) {
          this.segments[this.segments.length - 1] += 'M ';
        } else {
          this.segments[this.segments.length - 1] += ' L ';
        }
        this.segments[this.segments.length - 1] += coordinates[i][0] + ' ' + coordinates[i][1];
      }
      this.drawArrow(
        coordinates[coordinates.length - 1][0],
        coordinates[coordinates.length - 1][1],
        SVGPath.arrowDirection(coordinates[coordinates.length - 2], coordinates[coordinates.length - 1])
      );
    }
  }

  private formatTooltip(): string {
    let tooltipText: string = this.name.toUpperCase() + ' (' + this.width + ')';
    if (this.data.getValue() !== undefined && this.data.getValue() !== '') {
      tooltipText += ' - ' + this.data.getValue();
    }
    return tooltipText;
  }

  private parseJunctions(junctions: string[]): void {
    this.junctions = [];
    for (let junction of junctions) {
      let coordinates: number[] = junction.split(' ').map(Number);
      this.junctions.push(coordinates);
    }
  }

  private parsePoints(path: any): number[][] {
    let coordinates: number[][] = [];
    path.split(',').forEach((line: string) => {
      coordinates.push(line.trim().split(' ').map(Number));
    });
    return coordinates;
  }

  public equals(path: SVGPath): boolean {
    return this.name === path.name;
  }

  public inspect(): void {
    this.requestService.inspect([this.name.toLowerCase()]);
  }

  public parseEntity(entity: any): void {
    this.name = entity.name;
    this.width = entity.simulation.width;
    this.data = new BehaviorSubject<string>('');
    this.tooltip = new BehaviorSubject<string>(this.formatTooltip());
    this.data.subscribe(() => {
      this.tooltip.next(this.formatTooltip());
    });
    this.state = new BehaviorSubject<PathState>(PathState.Inactive);
    this.segments = [];
    for (let segment of entity.view.segments) {
      this.drawBus(this.parsePoints(segment));
    }
    if (entity.view.junctions) {
      this.parseJunctions(entity.view.junctions);
    }
  }

}
