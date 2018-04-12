import { Component, HostListener, Input } from '@angular/core';
import { Bus } from '../../../../models/simulator/bus/bus.model';
import { InspectService } from '../../../../services/simulator/inspect/inspect.service';

@Component({
  selector: 'marinade-bus-list-item',
  styleUrls: ['./bus-list-item.component.sass'],
  templateUrl: './bus-list-item.component.html',
})
export class BusListItemComponent {

  @Input('bus') public bus: Bus;

  constructor(private inspectService: InspectService) { }

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
    // todo move this into delete bus?
    this.bus.state.next('inactive');
    this.inspectService.deleteBus(this.bus);
  }

}
