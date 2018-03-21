interface Junction {
  x: number;
  y: number;
}

export interface Bus {
  data: string;
  junctions: Junction[];
  name: string;
  paths: string[];
  width: number;
}
