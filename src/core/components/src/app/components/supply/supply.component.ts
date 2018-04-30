import { Component, OnInit } from '@angular/core';
import { CardsService } from '../../services/cards/cards.service'
import { Card } from '../../services/models'

@Component({
  selector: 'app-supply',
  templateUrl: './supply.component.html',
  styleUrls: ['./supply.component.css']
})
export class SupplyComponent {

  cards: Card[] = [];

  constructor(public cardsService: CardsService) {
    this.cards = cardsService.getInitialSupply();
    console.log(this.cards);
  }

  getCardGroups() {
    const cardGroups = [];

    this.cards.forEach(card => {
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
