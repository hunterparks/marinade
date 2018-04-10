import { Component, HostListener } from '@angular/core';
import { Bus } from '../../../../models/simulator/bus/bus.model';
import { InspectService } from '../../../../services/simulator/inspect/inspect.service';

@Component({
  selector: 'marinade-bus-table',
  styleUrls: ['./bus-table.component.sass'],
  templateUrl: './bus-table.component.html',
})
export class BusTableComponent {

  public buses: Bus[] = [];
  public open: boolean = false;

  constructor(private inspect: InspectService) {
    inspect.buses.subscribe((buses: Bus[]) => {
      this.buses = buses;
    });
  }

  public getBuses(): void {
    this.buses = this.inspect.getBuses();
  }

  // Stop mouse events from being passed to the simulator view
  @HostListener('mousedown', ['$event'])
  @HostListener('mousemove', ['$event'])
  @HostListener('mouseup', ['$event'])
  @HostListener('mousewheel', ['$event'])
  public onMouseEvent(event: MouseWheelEvent): void {
    event.stopPropagation();
  }

  public toggleTab(): void {
    this.open = !this.open;
  }

}
