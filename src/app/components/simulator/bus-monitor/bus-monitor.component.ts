import { Component, HostListener } from '@angular/core';
import { Bus } from '@models/simulator/bus/bus.class';
import { BusMonitorService } from '@services/simulator/bus-monitor/bus-monitor.service';

@Component({
  selector: 'marinade-bus-monitor',
  styleUrls: ['./bus-monitor.component.sass'],
  templateUrl: './bus-monitor.component.html',
})
export class BusMonitorComponent {

  public buses: Bus[] = [];
  public open: boolean = false;

  constructor(private busMonitorService: BusMonitorService) {
    busMonitorService.buses.subscribe((buses: Bus[]) => {
      this.buses = buses;
    });
  }

  @HostListener('window:keyup', ['$event'])
  public onKeyUp(event: KeyboardEvent): void {
    switch (event.key) {
      case 'b': this.toggleTab();
    }
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
