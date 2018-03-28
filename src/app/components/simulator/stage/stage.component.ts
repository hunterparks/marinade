import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: '[svg-stage]',
  styleUrls: ['./stage.component.sass'],
  templateUrl: './stage.component.html',
})
export class StageComponent implements OnInit {

  public height: number;
  @Input('svg-stage') public register: any[];
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
