import { AfterViewInit, Component, ViewChild } from '@angular/core';

declare let $: any;

@Component({
  selector: 'marinade-editor',
  templateUrl: './editor.component.html',
  styleUrls: ['./editor.component.sass']
})
export class EditorComponent implements AfterViewInit {

  @ViewChild('editor') editor;
  public text: string = '';
  public mode: string = 'typescript';

  public ngAfterViewInit(): void {
    // $('#project-tree')
    //   .sidebar({
    //     context: $('#main-content'),
    //     closable: false,
    //     dimPage: false,
    //   });

    this.editor.setTheme('eclipse');

    this.editor.getEditor().setOptions({
      enableBasicAutocompletion: true
    });

    this.editor.getEditor().commands.addCommand({
      name: 'showOtherCompletions',
      bindKey: 'Ctrl-.',
    });
  }

}
