import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ServerService {

  gameId = location.pathname.split('/').pop()
  websocket = new WebSocket(`ws://${location.host}/api/game/${this.gameId}/`)

  public chatEvents: Subject<String> = new Subject();
  public logEvents: Subject<String> = new Subject();
  public updateEvents: Subject<Object> = new Subject();

  constructor() {
    window['debugSocket'] = this.websocket;
    window['sendSocketData'] = data => this.websocket.send(JSON.stringify(data));

    this.websocket.addEventListener('message', message => {
      console.log(message);
      const data = JSON.parse(message.data);
      if (!data.type) return;

      switch(data.type) {
        case 'chat':
          return this.chatEvents.next(data.payload);

        case 'log':
          return this.logEvents.next(data.payload);

        case 'update':
          return this.updateEvents.next(data.payload);
      }
    });
  }

  public sendChat(data: string) {
    const message = JSON.stringify({
      type: 'chat',
      payload: data
    });

    this.websocket.send(message);
  }

  public sendLog(data: string) {
    const message = JSON.stringify({
      type: 'log',
      payload: data
    });

    this.websocket.send(message);
  }

  public sendUpdate(data: object) {
    const message = JSON.stringify({
      type: 'update',
      payload: data
    });

    console.log(message);
    this.websocket.send(message);
  }






}
