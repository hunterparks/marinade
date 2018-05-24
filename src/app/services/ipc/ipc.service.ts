import { Injectable } from '@angular/core';
import { IpcRenderer } from 'electron';

@Injectable()
export class IpcService {

  private _ipc: IpcRenderer | undefined = void 0;

  constructor() {
    if (window.require) {
      try {
        this._ipc = window.require('electron').ipcRenderer;
      } catch (e) {
        throw e;
      }
    } else {
      // TODO: Fix this
      // tslint:disable-next-line:no-console
      console.warn('Electron\'s IPC was not loaded');
    }
  }

  public on(channel: string, listener: Function): void {
    if (!this._ipc) {
      return;
    }
    this._ipc.on(channel, listener);
  }

  public send(channel: string, ...args: any[]): void {
    if (!this._ipc) {
      return;
    }
    this._ipc.send(channel, ...args);
  }

}
