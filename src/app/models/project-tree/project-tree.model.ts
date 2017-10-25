export interface TreeNode {
  name: string;
  type: string;
  open: boolean;
  children?: TreeNode[];
}

export let ProjectFiles: TreeNode = {
  name: 'Marinade',
  type: 'folder',
  open: true,
  children: [
    {
      name: 'e2e',
      type: 'folder',
      open: false,
      children: [
        {
          name: 'app.e2e-spec.ts',
          type: 'ts',
          open: false,
        },
        {
          name: 'app.po.ts',
          type: 'ts',
          open: false,
        },
        {
          name: 'tsconfig.e2e.json',
          type: 'ts',
          open: false,
        },
      ]
    },
    {
      name: 'node_modules',
      type: 'folder',
      open: false,
    },
    {
      name: 'src',
      type: 'folder',
      open: true,
      children: [
        {
          name: 'app',
          type: 'folder',
          open: true,
          children: [
            {
              name: 'app.component.html',
              type: 'html',
              open: false,
            },
            {
              name: 'app.component.sass',
              type: 'sass',
              open: false,
            },
            {
              name: 'app.component.spec.ts',
              type: 'ts',
              open: false,
            },
            {
              name: 'app.component.ts',
              type: 'ts',
              open: false,
            },
            {
              name: 'app.module.ts',
              type: 'ts',
              open: false,
            },
          ]
        }
      ]
    }
  ]
};
