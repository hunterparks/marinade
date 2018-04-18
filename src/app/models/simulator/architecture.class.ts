import { Bus } from './bus/bus.class';
import { Controller } from './controller/controller.class';
import { Mux } from './mux/mux.class';
import { Register } from './register/register.class';
import { Stage } from './stage/stage.class';

export class Architecture {
  public bus?: Bus[];
  public controller?: Controller[];
  public mux?: Mux[];
  public stage?: Stage[];
  public stageRegister?: Register[];
}
