import { Component, EventEmitter, Output, ViewEncapsulation } from '@angular/core';

declare let $: any;

@Component({
  encapsulation: ViewEncapsulation.None,
  selector: 'marinade-menu-bar',
  templateUrl: './menu-bar.component.html',
  styleUrls: ['./menu-bar.component.sass']
})
export class MenuBarComponent {

  @Output() projectTreeToggle: EventEmitter<any> = new EventEmitter<any>();

  public toggleProjectTree(): void {
    this.projectTreeToggle.emit();
  }

}
