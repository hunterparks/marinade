import { Component, EventEmitter, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { TdCodeEditorComponent } from '@covalent/code-editor';
import 'rxjs/add/operator/takeUntil';
import { Subject } from 'rxjs/Subject';
import { EditorFileService } from '../../../services/editor/file/editor-file.service';
import { IpcService } from '../../../services/ipc/ipc.service';
import { WebsocketService } from '../../../services/simulator/websocket/websocket.service';
import { IFile } from '../../common/file-select/file-select/file-select.component';

@Component({
  selector: 'marinade-editor-view',
  styleUrls: ['./editor-view.component.scss'],
  templateUrl: './editor-view.component.html',
})
export class EditorViewComponent implements OnDestroy, OnInit {

  private _destroy: Subject<boolean>;
  private readonly FILE_FULL_PATH_INDEX: number = 0;
  private readonly FILE_NAME_EXTENSION_INDEX: number = 2;
  private readonly FILE_NAME_ONLY_INDEX: number = 3;
  private readonly FILE_PATH_INDEX: number = 1;
  @ViewChild(TdCodeEditorComponent) public monaco: TdCodeEditorComponent;

  constructor(
    private readonly _ipc: IpcService,
    private _file: EditorFileService,
    private _ws: WebsocketService
  ) {
    this._ws.connect();
  }

  public changedEditorValue(): void {
    this._file.updateContent(this.monaco.value);
  }

  public handleSaveClick(): void {
    if (this._file.getFileName()) { // File has name => file already exists
      this.ipcSaveFile(this._file.getFilePath() + this._file.getFileName(), this._file.getContent());
    } else { // File does not have name => file does not exist
      this.ipcSaveNewFile(this._file.getContent());
    }
  }

  public ipcSaveFile(fileFullPath: string, content: string): void {
    this._ipc.send('saveFile', fileFullPath, content);
  }

  public ipcSaveFileCallback(): void {
    this._file.updateDirtyFlag(false);
  }

  public ipcSaveNewFile(content: string): void {
    this._ipc.send('saveNewFile', content || '');
  }

  public ipcSaveNewFileCallback(filename: string): void {
    const fileInfo: RegExpMatchArray = filename.match(/(.*[\/\\])((.+)\..+)/);
    const fileFullPath: string = fileInfo[this.FILE_FULL_PATH_INDEX];
    const filePath: string = fileInfo[this.FILE_PATH_INDEX];
    const fileNameExtension: string = fileInfo[this.FILE_NAME_EXTENSION_INDEX];
    const fileNameOnly: string = fileInfo[this.FILE_NAME_ONLY_INDEX];
    this._file.updateFilename(fileNameExtension);
    this._file.updateFilepath(filePath);
    this._file.updateDirtyFlag(false);
  }

  public ngOnDestroy(): void {
    this._destroy.next(true);
    this._destroy.unsubscribe();
  }

  public ngOnInit(): void {
    // Create a boolean subject to mass-remove any subscriptions
    this._destroy = new Subject<boolean>();

    this._ws.messageSubject.takeUntil(this._destroy).subscribe((message: string) => {
      const response: any = JSON.parse(message);
    });

    this._ipc.on('saveFileCallback', (event: Electron.IpcMessageEvent) => {
      console.log('DEBUG: Save file callback');
      this.ipcSaveFileCallback();
    });
    this._ipc.on('saveNewFileCallback', (event: Electron.IpcMessageEvent, filename: string) => {
      console.log('DEBUG: Save new file callback');
      this.ipcSaveNewFileCallback(filename);
    });
    this._ipc.on('saveRequest', (event: Electron.IpcMessageEvent) => {
      this.handleSaveClick();
    });
    this._ipc.on('compileRequest', (event: Electron.IpcMessageEvent) => {
      const fullFilePath: string = this._file.getFilePath() + this._file.getFileName();
      // {'assemble':{'filepath':<'file'>}}
      const objectToSend: any = {
        assemble: { filepath: fullFilePath }
      };
      this._ws.write(JSON.stringify(objectToSend));
    });
    this._ipc.on('runRequest', (event: Electron.IpcMessageEvent) => {

    });

    // Subscribe to the editor's value change event
    this.monaco.onEditorValueChange
      .takeUntil(this._destroy)
      .subscribe(() => this.changedEditorValue());
  }

  public openFile(event: IFile): void {
    if (this._file.getDirtyFlag()) {

    } else {
      this.monaco.value = event.contents;
      this._file.updateContent(event.contents);
      this._file.updateFilename((event.name).substr(1));
      this._file.updateFilepath(event.path + (event.name).charAt(0));
      this._file.updateDirtyFlag(false);
    }
  }

}
