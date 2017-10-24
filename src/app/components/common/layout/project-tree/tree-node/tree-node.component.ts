import { Component, Input } from '@angular/core';
import { TreeNode } from '@models/project-tree/project-tree.model';

@Component({
  selector: 'marinade-tree-node',
  templateUrl: './tree-node.component.html',
  styleUrls: ['./tree-node.component.sass']
})
export class TreeNodeComponent {
  @Input() public node: TreeNode;
}
