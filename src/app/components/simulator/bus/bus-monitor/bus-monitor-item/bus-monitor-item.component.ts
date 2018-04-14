import { Component, HostListener, Input } from '@angular/core';
import { Bus } from '../../../../../models/simulator/bus/bus.class';
import { BusMonitorService } from '../../../../../services/simulator/bus-monitor/bus-monitor.service';

@Component({
  selector: 'marinade-bus-monitor-item',
  styleUrls: ['./bus-monitor-item.component.sass'],
  templateUrl: './bus-monitor-item.component.html',
})
export class BusMonitorItemComponent {

  @Input('bus') public bus: Bus;

  constructor(private busMonitorService: BusMonitorService) { }

  @HostListener('mouseenter')
  public onMouseEnter(): void {
    this.bus.state.next('active');
  }

  @HostListener('mouseleave')
  public onMouseLeave(): void {
    this.bus.state.next('inactive');
  }

  public removeBus(): void {
    // todo make variables for active/inactive
    this.bus.state.next('inactive');
    this.busMonitorService.deleteBus(this.bus);
  }

}
