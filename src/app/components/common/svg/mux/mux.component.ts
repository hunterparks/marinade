import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: '[svg-mux]',
  styleUrls: ['./mux.component.sass'],
  templateUrl: './mux.component.html',
})
export class MuxComponent implements OnInit {

  public static HEIGHT: number = 100;
  public static WIDTH: number = 40;

  @Input('svg-mux') public mux: any = null;
  public svg: string = '';

  private drawMux(): void {
    this.svg =   'M ' + (this.mux.x - MuxComponent.WIDTH / 2) + ' ' + (this.mux.y - MuxComponent.HEIGHT / 2);
    /*
    TODO: Will be used for ALU
    this.svg += ' L ' + (this.mux.x - MuxComponent.WIDTH / 2) + ' ' + (this.mux.y - MuxComponent.HEIGHT / 6);
    this.svg += ' L ' + (this.mux.x - MuxComponent.WIDTH / 4) + ' ' + (this.mux.y);
    this.svg += ' L ' + (this.mux.x - MuxComponent.WIDTH / 2) + ' ' + (this.mux.y + MuxComponent.HEIGHT / 6);
    */
    this.svg += ' L ' + (this.mux.x - MuxComponent.WIDTH / 2) + ' ' + (this.mux.y + MuxComponent.HEIGHT / 2);
    this.svg += ' L ' + (this.mux.x + MuxComponent.WIDTH / 2) + ' ' + (this.mux.y + MuxComponent.HEIGHT / 2 - 20);
    this.svg += ' L ' + (this.mux.x + MuxComponent.WIDTH / 2) + ' ' + (this.mux.y - MuxComponent.HEIGHT / 2 + 20);
    this.svg += ' Z';
  }

  public ngOnInit(): void {
    this.drawMux();
  }
}
