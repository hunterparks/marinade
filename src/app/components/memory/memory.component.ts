import { Component } from '@angular/core';
import { Register, Registers } from '@models/memory/register-values.model';

@Component({
  selector: 'marinade-memory',
  templateUrl: './memory.component.html',
  styleUrls: ['./memory.component.sass']
})
export class MemoryComponent {

  public text: string = 'code goes here';
  public registers: Register[] = Registers;

}
