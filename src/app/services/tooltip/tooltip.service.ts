import { Injectable } from '@angular/core';

@Injectable()
export class TooltipService {

  public tooltips: any[] = [];

  public findTooltip(id: number): any {
    return this.tooltips[this.findTooltipIndex(id)];
  }

  public findTooltipIndex(id: number): number {
    return this.tooltips.findIndex((tooltip: any) => {
      return tooltip.id === id;
    });
  }

  public remove(id: number): void {
    this.tooltips.splice(this.findTooltipIndex(id), 1);
  }

}
