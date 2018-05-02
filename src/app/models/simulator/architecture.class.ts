import { SVGRect } from '@models/simulator/svg/rect.svg.class';
import { Bus } from './bus/bus.class';
import { Mux } from './mux/mux.class';

export class Architecture {
  public bus?: Bus[];
  public combinational?: SVGRect[];
  public controller?: SVGRect[];
  public mux?: Mux[];
  public register?: SVGRect[];
  public stage?: SVGRect[];
}
