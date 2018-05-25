import { Component, HostListener, Input } from '@angular/core';
import { PathState, SVGPath } from '@models/simulator/svg/path.class';
import { BusMonitorService } from '@services/simulator/bus-monitor/bus-monitor.service';

@Component({
  selector: 'marinade-bus-monitor-item',
  styleUrls: ['./bus-monitor-item.component.sass'],
  templateUrl: './bus-monitor-item.component.html',
})
export class BusMonitorItemComponent {

  @Input('path') public path: SVGPath;
  public State: any = PathState;

  constructor(private busMonitorService: BusMonitorService) { }

  @HostListener('mouseenter')
  public onMouseEnter(): void {
    this.path.state.next(PathState.Active);
  }

  @HostListener('mouseleave')
  public onMouseLeave(): void {
    this.path.state.next(PathState.Inactive);
  }

  public removeBus(): void {
    this.path.state.next(PathState.Inactive);
    this.busMonitorService.deleteBus(this.path);
  }

}
