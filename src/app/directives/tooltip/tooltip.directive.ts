import { Directive, ElementRef, HostListener, Input, OnDestroy } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { TooltipService } from '../../services/tooltip/tooltip.service';

@Directive({ selector: '[tooltip]' })
export class TooltipDirective implements OnDestroy {

  private id: number;
  private toggled: boolean = false;
  @Input('tooltip') public content: BehaviorSubject<string>;

  constructor(private tooltipService: TooltipService, private element: ElementRef) { }

  private destroy(): void {
    this.tooltipService.remove(this.id);
  }

  public ngOnDestroy(): void {
    this.destroy();
  }

  @HostListener('dblclick', ['$event'])
  public onDoubleClick(): void {
    this.toggled = !this.toggled;
  }

  @HostListener('mouseenter', ['$event'])
  public onMouseEnter(event: MouseEvent): void {
    if (!this.toggled) {
      this.id = Math.random();
      this.tooltipService.tooltips.push({
        content: this.content,
        id: this.id,
        ref: this.element,
        x: new BehaviorSubject<number>(event.clientX),
        y: new BehaviorSubject<number>(event.clientY)
      });
    }
  }

  @HostListener('mouseleave')
  public onMouseLeave(): void {
    if (!this.toggled) {
      this.destroy();
    }
  }

  @HostListener('mousemove', ['$event'])
  public onMouseMove(event: MouseEvent): void {
    if (!this.toggled) {
      if (event.clientX !== this.tooltipService.findTooltip(this.id).x.getValue()) {
        this.tooltipService.findTooltip(this.id).x.next(event.clientX);
      }
      if (event.clientY !== this.tooltipService.findTooltip(this.id).y.getValue()) {
        this.tooltipService.findTooltip(this.id).y.next(event.clientY);
      }
    }
  }

}
