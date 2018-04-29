import { Bus } from './bus/bus.class';
import { Combinational } from './combinational/combinational.class';
import { Controller } from './controller/controller.class';
import { Mux } from './mux/mux.class';
import { Register } from './register/register.class';
import { Stage } from './stage/stage.class';

export class Architecture {
  public bus?: Bus[];
  public combinational?: Combinational[];
  public controller?: Controller[];
  public mux?: Mux[];
  public register?: Register[];
  public stage?: Stage[];
}
