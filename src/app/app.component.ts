import { Component } from '@angular/core';

@Component({
  selector: 'marinade-root',
  styleUrls: ['./app.component.css'],
  templateUrl: './app.component.html'
})
export class AppComponent {
  public title: string = 'app';

  constructor() {
    let thing: any = null;
    thing.thing();
  }
}
