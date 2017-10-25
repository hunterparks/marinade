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
    $('#project-tree')
      .sidebar({
        context: $('#main-content'),
        closable: false,
        dimPage: false,
      });
    $('#view-menu')
      .sidebar({
        context: $('#project-root'),
      });
  }

  toggleProjectTree() {
    $('#project-tree').sidebar('toggle');
  }

  toggleView() {
    $('#view-menu').sidebar({ transition: 'scale down' }).sidebar('toggle');
  }

}
