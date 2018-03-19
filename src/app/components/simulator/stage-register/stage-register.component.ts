import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: '[svg-stage-register]',
  styleUrls: ['./stage-register.component.sass'],
  templateUrl: './stage-register.component.html',
})
export class StageRegisterComponent implements OnInit {

  public height: number;
  @Input('svg-stage-register') public register: any[];
  public width: number;
  public x: number;
  public y: number;

  public ngOnInit(): void {
    this.height = this.register['height'];
    this.width = this.register['width'];
    this.x = this.register['x'];
    this.y = this.register['y'];
  }

}
