import { BehaviorSubject } from 'rxjs/BehaviorSubject';

interface Junction {
  x: number;
  y: number;
}

export interface Bus {
  data?: BehaviorSubject<string>;
  junctions: Junction[];
  name: string;
  paths: string[];
  state?: BehaviorSubject<string>;
  width: number;
}
