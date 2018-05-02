import { Component, ElementRef } from '@angular/core';
import { EventEmitter } from 'events';
import { Subject } from 'rxjs';
import { GameService } from './services/game/game.service';
import { ServerService } from './services/server/server.service';
import { CardsService } from './services/cards/cards.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  constructor(
    public game: GameService,
    private server: ServerService,
    private cards: CardsService,
  ) {


  }
}
