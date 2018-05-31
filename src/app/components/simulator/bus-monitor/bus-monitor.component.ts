import { Component, HostListener } from '@angular/core';
import { SVGPath } from '@models/simulator/svg/path.class';
import { BusMonitorService } from '@services/simulator/bus-monitor/bus-monitor.service';

@Component({
  selector: 'marinade-bus-monitor',
  styleUrls: ['./bus-monitor.component.sass'],
  templateUrl: './bus-monitor.component.html',
})
export class BusMonitorComponent {

  public open: boolean = false;
  public paths: SVGPath[] = [];

  constructor(private busMonitorService: BusMonitorService) {
    busMonitorService.paths.subscribe((paths: SVGPath[]) => {
      this.paths = paths;
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
