import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: '[svg-combinational]',
  styleUrls: ['./combinational.component.sass'],
  templateUrl: './combinational.component.html',
})
export class CombinationalComponent implements OnInit {

  @Input('svg-combinational') public combinational: any[];
  public height: number;
  public name: string;
  public width: number;
  public x: number;
  public y: number;

  public ngOnInit(): void {
    this.height = this.combinational['height'];
    this.width = this.combinational['width'];
    this.x = this.combinational['x'];
    this.y = this.combinational['y'];
  }

}
