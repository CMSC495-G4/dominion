import { Component, OnInit } from '@angular/core';
import { GameService } from '../../services/game/game.service';
import { Card } from '../../services/models';

@Component({
  selector: 'app-hand',
  templateUrl: './hand.component.html',
  styleUrls: ['./hand.component.css']
})
export class HandComponent {

  constructor(public game: GameService) {}


}
