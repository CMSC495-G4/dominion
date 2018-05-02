import { Component } from '@angular/core';
import { GameService } from '../../services/game/game.service';

@Component({
  selector: 'app-status',
  templateUrl: './status.component.html',
  styleUrls: ['./status.component.css']
})
export class StatusComponent {
  constructor(public game: GameService) {}
}
