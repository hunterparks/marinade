import { AfterViewInit, Component } from '@angular/core';

declare let $: any;

@Component({
  selector: 'marinade-root',
  templateUrl: './app.component.html',
  styleUrls: [ './app.component.sass' ]
})
export class AppComponent implements AfterViewInit {

  ngAfterViewInit() {
    // using context
    $('.ui.sidebar')
      .sidebar({
        context: $('.bottom.segment'),
        closable: false,
        dimPage: false,
      })
    ;
  }

  open() {
    $('.ui.sidebar').sidebar('toggle');
  }

}
