import { Component, EventEmitter, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
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
  private WS_QUEUE: string[] = [];
  @ViewChild(TdCodeEditorComponent) public monaco: TdCodeEditorComponent;

  constructor(
    private readonly _ipc: IpcService,
    private _file: EditorFileService,
    private _ws: WebsocketService,
    private _router: Router
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

    this.registerCustomLanguage();

    this._ws.messageSubject.takeUntil(this._destroy).subscribe((message: string) => {
      const response: { error?: string, status: boolean } = JSON.parse(message);
      const lastAction: string = this.WS_QUEUE.shift();
      if (lastAction === 'assembleRQ') {
        // TODO: Check error state
        if (response.status && !response.error) {
          const filePathToConfig: string = './src/config/architectures/pipeline_demo.json';
          // {'load':{'filepath':<'file'>}}
          const objectToSend: any = {
            load: { filepath: filePathToConfig }
          };
          this._ws.write(JSON.stringify(objectToSend));
          this.WS_QUEUE.push('loadRQ');
        } else {
          this._ipc.send('showError', 'Assemble Error', 'There was an error assembling machine code:\r\n\r\n' + response.error);
        }
      } else if (lastAction === 'loadRQ') {
        if (response.status && !response.error) {
          // TODO: Handle success
          this._ipc.send('showError', 'Success!', 'Ready to program!');
        } else {
          this._ipc.send('showError', 'Load Error', 'There was an error loading architecture:\r\n\r\n' + response.error);
        }
      } else if (lastAction === 'runRQ') {
        // TODO: Error Checking
        this._router.navigate(['simulator']);
      } else {
        this.WS_QUEUE.unshift(lastAction);
      }
    });

    this._ipc.on('saveFileCallback', (event: Electron.IpcMessageEvent) => {
      this.ipcSaveFileCallback();
    });
    this._ipc.on('saveNewFileCallback', (event: Electron.IpcMessageEvent, filename: string) => {
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
      this.WS_QUEUE.push('assembleRQ');
    });
    this._ipc.on('runRequest', (event: Electron.IpcMessageEvent) => {
      const filePathToMachineCode: string = './src/backend/assembler/generated_machine_code/machine_code.bin';
      // {'program':{'filepath':<'file'>,'memory':<'hook name'>}}
      const objectToSend: any = {
        program: {
          filepath: filePathToMachineCode,
          memory: 'progmem'
        }
      };
      this._ws.write(JSON.stringify(objectToSend));
      this.WS_QUEUE.push('runRQ');
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

  public registerCustomLanguage(): void {
    const customLanguage: any = {
      completionItemProvider: [
        {
          kind: 'monaco.languages.CompletionItemKind.Text',
          label: 'simpleText'
        },
        {
          insertText: 'testing({{condition}})',
          kind: 'monaco.languages.CompletionItemKind.Keyword',
          label: 'testing'
        },
        {
          documentation: 'If-Else Statement',
          insertText: [
            'if ({{condition}}) {',
            '\t{{}}',
            '} else {',
            '\t',
            '}',
          ].join('\n'),
          kind: 'monaco.languages.CompletionItemKind.Snippet',
          label: 'ifelse'
        },
      ],
      customTheme: {
        id: 'armAsmTheme',
        theme: {
          base: 'vs-dark',
          inherit: true,
          rules: [
            { token: 'custom-info', foreground: '808080' },
            { token: 'custom-error', foreground: 'ff0000', fontStyle: 'bold' },
            { token: 'custom-notice', foreground: 'FFA500' },
            { token: 'custom-date', foreground: '008800' },
          ],
        },
      },
      id: 'armAsm',
      monarchTokensProvider: [
        ['/\\[error.*/', 'custom-error'],
        ['/\\[notice.*/', 'custom-notice'],
        ['/\\[info.*/', 'custom-info'],
        ['/\\[[a-zA-Z 0-9:]+\\]/', 'custom-date'],
      ],
      monarchTokensProviderCSS: `
        .monaco-editor .token.custom-info {
          color: grey;
        }
        .monaco-editor .token.custom-error {
          color: red;
          font-weight: bold;
          font-size: 1.2em;
        }
        .monaco-editor .token.custom-notice {
          color: orange;
        }
        .monaco-editor .token.custom-date {
          color: green;
        }
      `
    };
    this.monaco.registerLanguage(customLanguage);
    this.monaco.theme = 'armAsmTheme';
    this.monaco.language = 'armAsm';
  }

}
