import { SVGRect } from '@models/simulator/svg/rect.svg.class';
import { Bus } from './bus/bus.class';
import { Mux } from './mux/mux.class';

// ALU
// ###############
// AluDemo,
// AluFlagRegister,
// AluFull,

// Rectangle
// ###############
// Constant,
// ControllerPipeline,
// ControllerSingleCycleDemo,
// ControllerSingleCycleFull,
// DataMemory,
// Exmem,
// Extender,
// HazardController,
// Idex,
// Ifid,
// Memory,
// MemoryReadSignExtender,
// Memwb,
// ProgramMemory,
// Register,
// RegisterFile,
// RegisterFileDemo,
// RegisterFileFull,
// Adder,

// Path
// ###############
// BusJoin,
// BusSubset,
// Bus,

// Mux
// ###############
// Mux,

// None?
// ###############
// Clock,
// LogicInput,
// Reset

export class Architecture {
  public bus?: Bus[];
  public combinational?: SVGRect[];
  public controller?: SVGRect[];
  public mux?: Mux[];
  public register?: SVGRect[];
  public stage?: SVGRect[];
}
