import { Component, HostListener, Input } from '@angular/core';
import { Bus, BusState } from '../../../../models/simulator/bus/bus.class';
import { BusMonitorService } from '../../../../services/simulator/bus-monitor/bus-monitor.service';

@Component({
  selector: 'marinade-bus-monitor-item',
  styleUrls: ['./bus-monitor-item.component.sass'],
  templateUrl: './bus-monitor-item.component.html',
})
export class BusMonitorItemComponent {

  @Input('bus') public bus: Bus;
  public State: any = BusState;

  constructor(private busMonitorService: BusMonitorService) { }

  @HostListener('mouseenter')
  public onMouseEnter(): void {
    this.bus.state.next(BusState.Active);
  }

  @HostListener('mouseleave')
  public onMouseLeave(): void {
    this.bus.state.next(BusState.Inactive);
  }

  public removeBus(): void {
    this.bus.state.next(BusState.Inactive);
    this.busMonitorService.deleteBus(this.bus);
  }

}
