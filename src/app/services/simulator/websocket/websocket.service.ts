
import { Injectable } from '@angular/core';
import { Subject } from 'rxjs/Subject';

@Injectable()
export class WebsocketService {

  private socket: any;
  public messageSubject: Subject<string>;

  /**
   * Simple constructor for the service, ensures all instance variables are initialized and connects the socket
   */
  constructor() {
    this.socket = null;
    this.messageSubject = new Subject<string>();
  }

  /**
   * onConnect is called when the socket connects, and logs that it has connected
   */
  private onConnect(): void {
    /* tslint:disable-next-line: no-console */ // Todo: Remove this output
    console.log('Connected');
  }

  /**
   * onDisconnect is called when the socket disconnects, and logs that it has disconnected
   */
  private onDisconnect(): void {
    /* tslint:disable-next-line: no-console */ // Todo: Remove this output
    console.log('Disconnected');
  }

  /**
   * This is called when the socket sees an error, and logs the event
   */
  private onError(event: Event): void {
    /* tslint:disable-next-line: no-console */ // Todo: Remove this output
    console.error('Socket error ' + event);
  }

  /**
   * onMessage is called whenever the socket reads data coming in
   * @param event The event that carries data in from the socket
   */
  private onMessage(event: Event): void {
    // Get the data
    this.messageSubject.next(event['data']);
  }

  /**
   * Connects the socket, is automatically called upon creation of the service
   * connection scheme differs depending upon device
   */
  public connect(): void {
    if (!this.isConnected()) {
      this.socket = new WebSocket('ws://localhost:4242');
      this.socket.onopen = this.onConnect.bind(this);
      this.socket.onclose = this.onDisconnect.bind(this);
      this.socket.onmessage = this.onMessage.bind(this);
      this.socket.onerror = this.onError.bind(this);
    }
  }

  /**
   * Disconnect disconnects the socket connection
   */
  public disconnect(): void {
    this.socket.close();
    this.socket = null;
  }

  /**
   * isConnected returns connection status on the socket.
   */
  public isConnected(): boolean {
    if (this.socket !== null && this.socket !== undefined && this.socket.readyState === 1) {
      return true;
    }
    return false;
  }

  /**
   * write writes data to the socket
   */
  public write(message: string): void {
    this.socket.send(message);
  }

}
