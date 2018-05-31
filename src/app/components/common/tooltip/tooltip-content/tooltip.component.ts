import { AfterContentInit, Component, Input, OnDestroy } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

@Component({
  selector: 'tooltip',
  styleUrls: ['./tooltip.component.sass'],
  templateUrl: './tooltip.component.html',
})
export class TooltipComponent implements AfterContentInit, OnDestroy {

  @Input() public content: BehaviorSubject<string>;
  public offsetX: number;
  public offsetY: number;
  @Input() public x: BehaviorSubject<number>;
  @Input() public y: BehaviorSubject<number>;

  public ngAfterContentInit(): void {
    this.x.subscribe((x: number) => {
      this.offsetX = x + 40;
    });
    this.y.subscribe((y: number) => {
      this.offsetY = y + 20;
    });
  }

  public ngOnDestroy(): void {
    this.x.unsubscribe();
    this.y.unsubscribe();
  }

}
