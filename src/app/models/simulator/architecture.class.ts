import { SVGPath } from '@models/simulator/svg/path.class';
import { SVGRect } from '@models/simulator/svg/rect.class';
import { SVGTrapezoid } from '@models/simulator/svg/trapezoid.class';

export class Architecture {
  public path?: SVGPath[];
  public rectangle?: SVGRect[];
  public trapezoid?: SVGTrapezoid[];
}
