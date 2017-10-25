import { AfterViewInit, Component } from '@angular/core';

declare let $: any;

@Component({
  selector: 'marinade-root',
  templateUrl: './app.component.html',
  styleUrls: [ './app.component.sass' ]
})
export class AppComponent implements AfterViewInit {

  ngAfterViewInit() {
    $('#view-menu')
      .sidebar({
        context: $('#project-root'),
      });
  }

  toggleView() {
    $('#view-menu').sidebar({ transition: 'scale down' }).sidebar('toggle');
  }

}
