import { Component, ViewEncapsulation } from '@angular/core';

declare let $: any;

@Component({
  encapsulation: ViewEncapsulation.None,
  selector: 'marinade-menu-bar',
  templateUrl: './menu-bar.component.html',
  styleUrls: ['./menu-bar.component.sass']
})
export class MenuBarComponent { }
