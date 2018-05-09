import { Component, HostListener, Input, OnInit } from '@angular/core';
import { Bus, BusState } from '../../../../models/simulator/bus/bus.class';
import { BusMonitorService } from '../../../../services/simulator/bus-monitor/bus-monitor.service';

@Component({
  selector: '[svg-bus]',
  styleUrls: ['./bus.component.sass'],
  templateUrl: './bus.component.html',
})
export class BusComponent implements OnInit {

  private static DEFAULT_COLOR: string = 'deepskyblue';
  private static HIGHLIGHT_COLOR: string = '#ff0000';
  private static SELECT_COLOR: string = '#00ff00';

  @Input('svg-bus') public bus: Bus = null;
  public color: string = BusComponent.DEFAULT_COLOR;

  constructor(private busMonitorService: BusMonitorService) { }

  public ngOnInit(): void {
    this.bus.state.subscribe((state: BusState) => {
      switch (state) {
        case BusState.Active: this.color = BusComponent.HIGHLIGHT_COLOR; break;
        case BusState.Inactive: this.color = BusComponent.DEFAULT_COLOR; break;
        default: this.color = BusComponent.DEFAULT_COLOR;
      }
    });
  }

  @HostListener('click')
  public onClick(): void {
    this.color = BusComponent.SELECT_COLOR;
  }

  @HostListener('dblclick')
  public onDoubleClick(): void {
    if (!this.busMonitorService.deleteBus(this.bus)) {
      this.busMonitorService.addBus(this.bus);
    }
  }

  @HostListener('mouseenter')
  public onMouseEnter(): void {
    this.bus.inspect();
    this.bus.state.next(BusState.Active);
  }

  @HostListener('mouseleave')
  public onMouseLeave(): void {
    this.bus.state.next(BusState.Inactive);
  }

}
