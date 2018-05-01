import { Component, ElementRef } from '@angular/core';
import { EventEmitter } from 'events';
import { Subject } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  websocket: WebSocket;
  chatEvents = new Subject();
  logEvents = new Subject();
  updateEvents = new Subject();

  state;

  constructor({nativeElement}: ElementRef) {
    let gameId = +nativeElement.getAttribute('game-id');
    let userId = +nativeElement.getAttribute('user-id');
    let userName = nativeElement.getAttribute('user-name');
    let players = nativeElement.getAttribute('players').split(',');
  }
}
