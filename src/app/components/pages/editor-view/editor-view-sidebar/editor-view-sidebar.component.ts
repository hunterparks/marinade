import { Component } from '@angular/core';
import { IpcService } from '@services/ipc/ipc.service';

@Component({
  selector: 'marinade-editor-view-sidebar',
  styleUrls: ['./editor-view-sidebar.component.sass'],
  templateUrl: './editor-view-sidebar.component.html',
})
export class EditorViewSidebarComponent {

  private readonly SIDEBAR_CONFIG: any = [
    { callingID: 'save',    icon: 'floppy-o', title: 'Save'     },
    { callingID: 'compile', icon: 'cogs',     title: 'Compile'  },
    { callingID: 'run',     icon: 'play',     title: 'Run'      }
  ];

  constructor(
    private _ipc: IpcService
  ) {}

  public sidebarClickHandler(source: string): void {
    this._ipc.send(source + 'Request');
  }

}
