import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { Message, GameState } from '../models'

@Injectable({
  providedIn: 'root'
})
export class ServerService {

  gameId = location.pathname.split('/').pop()
  websocket = new WebSocket(`ws://${location.host}/api/game/${this.gameId}/`)
  queue: string[] = [];

  public chatEvents: Subject<Message> = new Subject();
  public logEvents: Subject<String> = new Subject();
  public updateEvents: Subject<GameState> = new Subject();

  constructor() {
    window['debugSocket'] = this.websocket;
    window['sendSocketData'] = data => this.websocket.send(JSON.stringify(data));

    this.websocket.addEventListener('open', ev => {
      while (this.queue.length)
        this.websocket.send(this.queue.shift())
    })

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

  sendMessage(message) {
    if (this.websocket.readyState == 1) {
      this.websocket.send(message);
    } else {
      this.queue.push(message);
    }
  }

  public sendChat(data: Message) {
    const message = JSON.stringify({
      type: 'chat',
      payload: data
    });

    this.sendMessage(message);
  }

  public sendLog(data: string) {
    const message = JSON.stringify({
      type: 'log',
      payload: data
    });

    this.sendMessage(message);
  }

  public sendUpdate(data: GameState) {
    const message = JSON.stringify({
      type: 'update',
      payload: data
    });

    console.log(message);
    this.sendMessage(message);
  }






}
