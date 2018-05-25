import { Component } from '@angular/core';
import { SVGPath } from '@models/simulator/svg/path.class';
import { ArchitectureService } from '@services/simulator/architecture/architecture.service';
import { RequestService } from '@services/simulator/request/request.service';

@Component({
  selector: 'marinade-simulator-view-sidebar',
  styleUrls: ['./simulator-view-sidebar.component.sass'],
  templateUrl: './simulator-view-sidebar.component.html',
})
export class SimulatorViewSidebarComponent {

  public readonly SIDEBAR_CONFIG: any = [
    { callingID: 'load',   icon: 'folder-open-o',  title: 'Load'   },
    { callingID: 'reset',  icon: 'undo',           title: 'Reset'  },
    { callingID: 'unload', icon: 'times-circle-o', title: 'Unload' },
    { callingID: 'spacer', icon: '',               title: ''       },
    { callingID: 'step',   icon: 'step-forward',   title: 'Step'   },
  ];

  constructor(private architectureService: ArchitectureService, private requestService: RequestService) { }

  public sidebarClickHandler(source: string): void {
    switch (source) {
      case 'load': this.architectureService.load(); break;
      case 'unload': this.architectureService.unload(); break;
      case 'step':
        this.requestService.step('logic');
        this.architectureService.architecture.getValue().path.forEach((path: SVGPath) => {
          path.inspect();
        });
        break;
      default: break;
    }
  }

}
