import { Component, OnInit } from '@angular/core';
import { CardsService } from '../../services/cards/cards.service'
import { Card } from '../../services/models'
import { GameService } from '../../services/game/game.service';

@Component({
  selector: 'app-supply',
  templateUrl: './supply.component.html',
  styleUrls: ['./supply.component.css']
})
export class SupplyComponent {

  cards: Card[] = [];

  constructor(
    public game: GameService,
    public cardsService: CardsService) {
    this.cards = this.game.state.supply;
  }

  getCardGroups() {
    const cardGroups = [];

    this.game.state.supply.forEach(card => {
      const group = cardGroups.find(groupedCard =>
        groupedCard.name == card.name);

      if (group == undefined) {
        cardGroups.push({
          ...card,
          quantity: 1
        });
      } else {
        group.quantity ++;
      }
    });

    cardGroups.sort((a, b) => b.type.localeCompare(a.type) || a.cost - b.cost);


    return cardGroups;
  }

  buyCard(cardName: string) {
    let card = this.cards.find(card => card.name == cardName);
    let index = this.cards.indexOf(card);
    this.cards.splice(index, 1);
  }

}
