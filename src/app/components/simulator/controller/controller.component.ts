import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: '[svg-controller]',
  styleUrls: ['./controller.component.sass'],
  templateUrl: './controller.component.html',
})
export class ControllerComponent implements OnInit {

  public height: number;
  @Input('svg-controller') public register: any[];
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
