import { Component, HostListener, Input, OnInit } from '@angular/core';
import { PathState, SVGPath } from '@models/simulator/svg/path.class';
import { BusMonitorService } from '@services/simulator/bus-monitor/bus-monitor.service';

@Component({
  selector: '[svg-path]',
  styleUrls: ['./path.component.sass'],
  templateUrl: './path.component.html',
})
export class PathComponent implements OnInit {

  private static DEFAULT_COLOR: string = 'deepskyblue';
  private static HIGHLIGHT_COLOR: string = '#ff0000';
  private static SELECT_COLOR: string = '#00ff00';

  public color: string = PathComponent.DEFAULT_COLOR;
  @Input('svg-path') public path: SVGPath = null;

  constructor(private busMonitorService: BusMonitorService) { }

  public ngOnInit(): void {
    this.path.state.subscribe((state: PathState) => {
      switch (state) {
        case PathState.Active: this.color = PathComponent.HIGHLIGHT_COLOR; break;
        case PathState.Inactive: this.color = PathComponent.DEFAULT_COLOR; break;
        default: this.color = PathComponent.DEFAULT_COLOR;
      }
    });
  }

  @HostListener('click')
  public onClick(): void {
    this.color = PathComponent.SELECT_COLOR;
  }

  @HostListener('dblclick')
  public onDoubleClick(): void {
    // TODO: fix bus monitor
    if (!this.busMonitorService.deleteBus(this.path)) {
      this.busMonitorService.addBus(this.path);
    }
  }

  @HostListener('mouseenter')
  public onMouseEnter(): void {
    this.path.inspect();
    this.path.state.next(PathState.Active);
  }

  @HostListener('mouseleave')
  public onMouseLeave(): void {
    this.path.state.next(PathState.Inactive);
  }

}
