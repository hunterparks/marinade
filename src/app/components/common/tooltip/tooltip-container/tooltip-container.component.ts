import { Component } from '@angular/core';
import { TooltipService } from '../../../../services/tooltip/tooltip.service';

@Component({
  selector: 'tooltip-container',
  styleUrls: ['./tooltip-container.component.sass'],
  templateUrl: './tooltip-container.component.html',
})
export class TooltipContainerComponent {

  public tooltips: any[];

  constructor(tooltipService: TooltipService) {
    this.tooltips = tooltipService.tooltips;
  }

}
