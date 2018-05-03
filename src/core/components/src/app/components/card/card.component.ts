import { Component, Input, Output, EventEmitter } from '@angular/core';
import { Card } from '../../services/models';
import { GameService } from '../../services/game/game.service';

@Component({
  selector: 'app-card',
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.css']
})
export class CardComponent {

  @Input('card')
  card: Card;

  constructor(public game: GameService) {}
}
