import { Inject } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { RequestService } from '../../../services/simulator/request/request.service';
import { SimulatorComponent } from '../simulator-component.class';

interface Junction {
  x: number;
  y: number;
}

export class Bus extends SimulatorComponent {
  public data?: BehaviorSubject<string>;
  public junctions: Junction[];
  public name: string;
  public paths: string[];
  public state?: BehaviorSubject<string>;
  public tooltip: BehaviorSubject<string>;
  public width: number;

  constructor (@Inject(RequestService) private requestService: RequestService, bus: Bus) {
    super();
    this.junctions = bus.junctions;
    this.name = bus.name;
    this.paths = bus.paths;
    this.width = bus.width;
    this.initialize();
    this.data.subscribe(() => {
      this.tooltip.next(this.formatTooltip());
    });
  }

  private formatTooltip(): string {
    let tooltipText: string = this.name + ' (' + this.width + ')';
    if (this.data !== undefined) {
      tooltipText += ' - ' + this.data.getValue();
    }
    return tooltipText;
  }

  public equals(bus: Bus): boolean {
    return this.name === bus.name;
  }

  public initialize(): void {
    this.data = new BehaviorSubject<string>('');
    this.state = new BehaviorSubject<string>('inactive');
    this.tooltip = new BehaviorSubject<string>(this.formatTooltip());
  }

  public inspect(): void {
    this.requestService.inspect([this.name.toLowerCase()]);
  }
}
