import { Injectable } from '@angular/core';
import { WebsocketService } from '../websocket/websocket.service';

@Injectable()
export class RequestService {

  // register - state
  // register file - start, data
  // memory - start, data

  constructor (private websocketService: WebsocketService) { }

  public clear(components: string[]): void {
    // not all components have clear - only memory-type objects (reg, reg files, memory)
  }

  public generate(components: string[], parameters: string[]): void {
    // buses, clocks, resets, etc.
  }

  public inspect(components: string[]): void {
    this.websocketService.write('{ "inspect": ' + JSON.stringify(components) + ' }');
  }

  public load(filepath: string): void {
    // TODO - add file chooser
    this.websocketService.write('{ "load": { "filepath": "pipeline_poc.json" } }');
  }

  public modify(component: string, parameters: string[]): void {
    // not all components have modify - only memory-type objects (reg, reg files, memory)
  }

  public program(filepath: string, memory: string): void {
    // TODO - add file chooser
    this.websocketService.write('{ "program": { "filepath": "", "memory": "progmem" } }');
  }

  public reset(): void {
    this.websocketService.write('{ "reset": {} }');
  }

  public step(type: string = 'edge'): void {
    // if (type === 'edge') {
      // step twice
    // }
    this.websocketService.write('{ "step": { "type": "' + type + '" } }');
  }

  public unload(): void {
    this.websocketService.write('{ "unload": {} }');
  }

}
