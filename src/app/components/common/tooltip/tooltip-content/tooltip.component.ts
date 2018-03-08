import { Component, ElementRef, Input, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

@Component({
  selector: 'tooltip',
  styleUrls: ['./tooltip.component.sass'],
  templateUrl: './tooltip.component.html',
})
export class TooltipComponent implements OnInit, OnDestroy {

  @Input() public content: string;
  @ViewChild('tooltip') public element: ElementRef;
  public offsetX: number;
  public offsetY: number;
  @Input() public x: BehaviorSubject<number>;
  @Input() public y: BehaviorSubject<number>;

  public ngOnDestroy(): void {
    this.x.unsubscribe();
    this.y.unsubscribe();
  }

  public ngOnInit(): void {
    this.x.subscribe((x: number) => {
      this.offsetX = x - 12;
    });
    this.y.subscribe((y: number) => {
      this.offsetY = y - 44;
    });
  }

}
