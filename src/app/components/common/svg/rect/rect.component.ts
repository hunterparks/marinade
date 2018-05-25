import { Component, Input, OnInit } from '@angular/core';
import { SVGRect } from '@models/simulator/svg/rect.class';

@Component({
  selector: '[svg-rect]',
  styleUrls: ['./rect.component.sass'],
  templateUrl: './rect.component.html',
})
export class RectComponent implements OnInit {

  public color: string;
  public fontSize: number = 10;
  @Input('svg-rect') public rect: SVGRect;

  public ngOnInit(): void {
    switch (this.rect.type) {
      case 'combinational':
        this.color = '#ffaa33'; break;
      case 'memwb':
      case 'exmem':
      case 'idex':
      case 'ifid':
        this.color = '#00ff33'; break;
      case 'controllerpipeline':
      case 'hazardcontroller':
        this.color = '#ffff00'; break;
      case 'datamemory':
      case 'stage':
        this.color = '#ff0000'; break;
      default:       this.color = '#cccccc';
    }
  }

}
