import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: '[svg-label]',
  styleUrls: ['./label.component.sass'],
  templateUrl: './label.component.html',
})
export class LabelComponent implements OnInit {

  @Input('svg-label') public label: any = null;
  public size: string = '12px';
  public text: string = '';
  public x: number;
  public y: number;

  public ngOnInit(): void {
    this.size = this.label['size'];
    this.text = this.label['text'];
    this.x = this.label['x'];
    this.y = this.label['y'];
  }

}
