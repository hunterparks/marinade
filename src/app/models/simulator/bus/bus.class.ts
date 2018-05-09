import { Inject } from '@angular/core';
import { RequestService } from '@services/simulator/request/request.service';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

export enum BusState {
  Active,
  Inactive
}

interface Junction {
  x: number;
  y: number;
}

interface Path {
  points: string;
  startBit: number;
  width: number;
}

export class Bus {
  public arrows: string[] = [];
  public data?: BehaviorSubject<string>;
  public junctions: Junction[];
  public name: string;
  public paths: (Path | string)[];
  public state?: BehaviorSubject<BusState>;
  public tooltip: BehaviorSubject<string>;
  public width: number;

  constructor(@Inject(RequestService) private requestService: RequestService, bus: Bus) {
    this.initialize(bus);
    this.data.subscribe(() => {
      this.tooltip.next(this.formatTooltip());
    });
  }

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
      this.paths.push('');
      for (let i: number = 0; i < coordinates.length; i++) {
        if (i === 0) {
          this.paths[this.paths.length - 1] += 'M ';
        } else {
          this.paths[this.paths.length - 1] += ' L ';
        }
        this.paths[this.paths.length - 1] += coordinates[i][0] + ' ' + coordinates[i][1];
      }
      this.drawArrow(
        coordinates[coordinates.length - 1][0],
        coordinates[coordinates.length - 1][1],
        Bus.arrowDirection(coordinates[coordinates.length - 2], coordinates[coordinates.length - 1])
      );
    }
  }

  private formatTooltip(): string {
    let tooltipText: string = this.name + ' (' + this.width + ')';
    if (this.data.getValue() !== undefined && this.data.getValue() !== '') {
      tooltipText += ' - ' + this.data.getValue();
    }
    return tooltipText;
  }

  private parsePoints(path: any): number[][] {
    let coordinates: number[][] = [];
    if (typeof path === 'string') {
      path.split(',').forEach((line: string) => {
        coordinates.push(line.trim().split(' ').map(Number));
      });
    }
    return coordinates;
  }

  public equals(bus: Bus): boolean {
    return this.name === bus.name;
  }

  public initialize(bus: Bus): void {
    this.junctions = bus.junctions;
    this.name = bus.name;
    this.paths = [];
    this.width = bus.width;
    this.data = new BehaviorSubject<string>('');
    this.state = new BehaviorSubject<BusState>(BusState.Inactive);
    this.tooltip = new BehaviorSubject<string>(this.formatTooltip());
    for (let path of bus.paths) {
      this.drawBus(this.parsePoints(path));
    }
  }

  public inspect(): void {
    this.requestService.inspect([this.name.toLowerCase()]);
  }
}
