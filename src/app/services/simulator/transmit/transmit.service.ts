import { Injectable } from '@angular/core';
import { WebsocketService } from '../websocket/websocket.service';

@Injectable()
export class TransmitService {

  // register - state
  // register file - start, data
  // memory - start, data

  constructor(private websocket: WebsocketService) {}

  public clear(components: string[]): void {
    // not all components have clear - only memory-type objects (reg, reg files, memory)
  }

  public generate(components: string[], parameters: string[]): void {
    // buses, clocks, resets, etc.
  }

  public inspect(components: string[]): void {
    this.websocket.write('{ "inspect": ' + JSON.stringify(components) + ' }');
  }

  public load(filepath: string): void {
    // TODO - add file chooser
    this.websocket.write('{ "load": { "filepath": "pipeline_poc.json" } }');
  }

  public modify(component: string, parameters: string[]): void {
    // not all components have modify - only memory-type objects (reg, reg files, memory)
  }

  public program(filepath: string, memory: string): void {
    // TODO - add file chooser
    this.websocket.write('{ "program": { "filepath": "", "memory": "progmem" } }');
  }

  public reset(): void {
    this.websocket.write('{ "reset": {} }');
  }

  public step(type: string = 'edge'): void {
    // if (type === 'edge') {
      // step twice
    // }
    this.websocket.write('{ "step": { "type": "' + type + '" } }');
  }

  public unload(): void {
    this.websocket.write('{ "unload": {} }');
  }

}
