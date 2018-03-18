import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: '[svg-register]',
  styleUrls: ['./register.component.sass'],
  templateUrl: './register.component.html',
})
export class RegisterComponent implements OnInit {

  public color: string;
  public height: number;
  @Input('svg-register') public register: any[];
  public width: number;
  public x: number;
  public y: number;

  public ngOnInit(): void {
    this.color = this.register['color'];
    this.height = this.register['height'];
    this.width = this.register['width'];
    this.x = this.register['x'];
    this.y = this.register['y'];
  }

}
