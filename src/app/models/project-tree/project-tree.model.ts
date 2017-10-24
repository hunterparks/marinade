export class TreeNode {
  public name: string;
  public type: string;
  public status: string;
  public children?: TreeNode[];
}

export const ProjectFiles: TreeNode = {
  name: 'Marinade',
  type: 'folder',
  status: 'open',
  children: [
    {
      name: 'e2e',
      type: 'folder',
      status: 'closed',
      children: [
        {
          name: 'app.e2e-spec.ts',
          type: 'ts',
          status: 'closed',
        },
        {
          name: 'app.po.ts',
          type: 'ts',
          status: 'closed',
        },
        {
          name: 'tsconfig.e2e.json',
          type: 'ts',
          status: 'closed',
        },
      ]
    },
    {
      name: 'node_modules',
      type: 'folder',
      status: 'closed',
    },
    {
      name: 'src',
      type: 'folder',
      status: 'open',
      children: [
        {
          name: 'app',
          type: 'folder',
          status: 'open',
          children: [
            {
              name: 'app.component.html',
              type: 'html',
              status: 'closed',
            },
            {
              name: 'app.component.sass',
              type: 'sass',
              status: 'closed',
            },
            {
              name: 'app.component.spec.ts',
              type: 'ts',
              status: 'closed',
            },
            {
              name: 'app.component.ts',
              type: 'ts',
              status: 'closed',
            },
            {
              name: 'app.module.ts',
              type: 'ts',
              status: 'closed',
            },
          ]
        }
      ]
    }
  ]
};
