import { Directive, ElementRef, HostListener, Input, OnDestroy } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { TooltipService } from '../../services/tooltip/tooltip.service';

@Directive({ selector: '[tooltip]' })
export class TooltipDirective implements OnDestroy {

  private id: number;
  @Input('tooltip') public content: BehaviorSubject<string>;

  constructor(private tooltip: TooltipService, private element: ElementRef) { }

  private destroy(): void {
    this.tooltip.remove(this.id);
  }

  public ngOnDestroy(): void {
    this.destroy();
  }

  @HostListener('mouseenter', ['$event'])
  public onMouseEnter(event: MouseEvent): void {
    this.id = Math.random();
    this.tooltip.tooltips.push({
      content: this.content,
      id: this.id,
      ref: this.element,
      x: new BehaviorSubject<number>(event.clientX),
      y: new BehaviorSubject<number>(event.clientY)
    });
  }

  @HostListener('mouseleave')
  public onMouseLeave(): void {
    this.destroy();
  }

  @HostListener('mousemove', ['$event'])
  public onMouseMove(event: MouseEvent): void {
    if (event.clientX !== this.tooltip.findTooltip(this.id).x.getValue()) {
      this.tooltip.findTooltip(this.id).x.next(event.clientX);
    }
    if (event.clientY !== this.tooltip.findTooltip(this.id).y.getValue()) {
      this.tooltip.findTooltip(this.id).y.next(event.clientY);
    }
  }

}
