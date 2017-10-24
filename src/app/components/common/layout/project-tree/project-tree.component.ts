import { Component } from '@angular/core';
import { ProjectFiles, TreeNode } from '@models/project-tree/project-tree.model';

@Component({
  selector: 'marinade-project-tree',
  templateUrl: './project-tree.component.html',
  styleUrls: ['./project-tree.component.sass']
})
export class ProjectTreeComponent {

  public files: TreeNode = ProjectFiles;

}
