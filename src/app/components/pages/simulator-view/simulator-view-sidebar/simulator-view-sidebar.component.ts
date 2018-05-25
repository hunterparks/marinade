import { Component } from '@angular/core';
import { ArchitectureService } from '@services/simulator/architecture/architecture.service';

@Component({
  selector: 'marinade-simulator-view-sidebar',
  styleUrls: ['./simulator-view-sidebar.component.sass'],
  templateUrl: './simulator-view-sidebar.component.html',
})
export class SimulatorViewSidebarComponent {

  private readonly SIDEBAR_CONFIG: any = [
    { callingID: 'load',   icon: 'folder-open-o',  title: 'Load'   },
    { callingID: 'reset',  icon: 'undo',           title: 'Reset'  },
    { callingID: 'unload', icon: 'times-circle-o', title: 'Unload' },
    { callingID: 'spacer', icon: '',               title: ''       },
    { callingID: 'step',   icon: 'step-forward',   title: 'Step'   },
  ];

  constructor(private architectureService: ArchitectureService) { }

  public sidebarClickHandler(source: string): void {
    switch (source) {
      case 'load': this.architectureService.load(); break;
      case 'unload': this.architectureService.unload(); break;
      default: break;
    }
  }

}
