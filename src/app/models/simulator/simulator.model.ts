import { Bus } from './bus/bus.model';
import { Controller } from './controller/controller.model';
import { Mux } from './mux/mux.model';
import { Register } from './register/register.model';
import { Stage } from './stage/stage-register.model';

export interface Simulator {
  bus?: Bus[];
  controller?: Controller[];
  mux?: Mux[];
  stage?: Stage[];
  stageRegister?: Register[];
}
