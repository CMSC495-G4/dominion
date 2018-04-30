import { Injectable } from '@angular/core';
import { GameState, Card, Player } from '../models';

@Injectable({
  providedIn: 'root'
})
export class CardsService {
  /** http://dominion.diehrstraits.com/?set=All&f=list */

  cards: Card[] = [
    {
      name: 'copper',
      cost: 0,
      type: 'treasure',
      value: 1,
    },
    {
      name: 'silver',
      cost: 3,
      type: 'treasure',
      value: 2,
    },
    {
      name: 'gold',
      cost: 6,
      type: 'treasure',
      value: 3,
    },

    {
      name: 'estate',
      cost: 2,
      type: 'victory',
      value: 1,
    },
    {
      name: 'duchy',
      cost: 5,
      type: 'victory',
      value: 3,
    },
    {
      name: 'province',
      cost: 8,
      type: 'victory',
      value: 6,
    },

    {
      name: 'curse',
      cost: 0,
      type: 'curse',
      value: -1,
    },


    {
      name: 'cellar',
      cost: 2,
      type: 'action',
      reducer: async (state: GameState)  => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);
        const currentPlayer = newState.players
          [state.turn % state.players.length];

        // allow the player to select all the cards in their hand
        const selection = await this.getSelection(
          currentPlayer,
          currentPlayer.hand.length
        );

        // remove the cards from the player's hand
        currentPlayer.hand = currentPlayer.hand
          .filter(card => !selection.includes(card));

        // put these cards in the player's deck
        currentPlayer.deck.push(...selection);

        // shuffle the player's deck
        currentPlayer.deck = this.shuffle(currentPlayer.deck);

        // draw an equal number of cards as the selection
        for (let i = 0; i < selection.length; i ++) {
          const card = currentPlayer.deck.pop();
        }

        return newState;
      }
    },

    {
      name: 'chapel',
      cost: 2,
      type: 'action',
      reducer: async (state: GameState) => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);
        const currentPlayer = newState.players
          [state.turn % state.players.length];

        // allow the player to select up to four cards
        const selection = await this.getSelection(currentPlayer, 4);

        // remove the cards from the player's hand
        currentPlayer.hand = currentPlayer.hand
          .filter(card => !selection.includes(card));

        // put these cards in the trash
        currentPlayer.trash.push(...selection);

        return newState;
      }
    },

    {// note: if the moat is in a player's hand, it will nullify an attack
     // this is different from the base game's behavior
      name: 'moat',
      cost: 2,
      type: 'action',
      reducer: async (state: GameState)  => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);
        const currentPlayer = newState.players
          [state.turn % state.players.length];

          for (let i = 0; i < 2; i ++) {
            const card = currentPlayer.deck.pop();
            currentPlayer.hand.push(card);
          }

        return newState;
      }
    },

    {
      name: 'chancellor',
      cost: 3,
      type: 'action',
      reducer: async (state: GameState)  =>  {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);
        const currentPlayer = newState.players
          [state.turn % state.players.length];

        // puts the player's discard pile into their deck
        while (currentPlayer.discard.length > 0) {
          currentPlayer.deck.push(
            currentPlayer.discard.pop()
          );
        }

        // shuffle the player's deck
        currentPlayer.deck = this.shuffle(currentPlayer.deck);

        return newState;
      }
    },

    {
      name: 'village',
      cost: 3,
      type: 'action',
      reducer: async (state: GameState) =>  {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);
        const currentPlayer = newState.players
          [state.turn % state.players.length];

        // +1 card
        const card = currentPlayer.deck.pop();
        newState.log.push(`${currentPlayer.name} drew: ${card.name}`);
        currentPlayer.hand.push(card);

        // +2 actions
        currentPlayer.actions += 2;
        return newState;
      }
    },

    {
      name: 'woodcutter',
      cost: 3,
      type: 'action',
      reducer: async (state: GameState)  => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);
        const currentPlayer = newState.players
          [state.turn % state.players.length];

        // +1 buy
        currentPlayer.buys += 1;

        // +2 coins
        currentPlayer.coins += 2;
        return newState;
      }
    },



    {
      name: 'workshop',
      cost: 3,
      type: 'action',
      reducer: async (state: GameState) =>  {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);
        const currentPlayer = newState.players
          [state.turn % state.players.length];

        // +4 coins
        currentPlayer.coins += 4;
        return newState;
      }
    },



    {
      name: 'witch',
      cost: 0,
      type: 'action',
      value: 1,
      reducer: async (state: GameState) => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);
        const currentPlayer = newState.players
          [state.turn % state.players.length];

        newState.log.push(`${currentPlayer.name} played: witch.`);
        currentPlayer.actions --;

        for (let i = 0; i < 2; i ++) {
          const card = currentPlayer.deck.pop();
          newState.log.push(`${currentPlayer.name} drew: ${card.name}`);
          currentPlayer.hand.push(card);
        }

        newState.players
          .filter(player => player.id != currentPlayer.id)
          .filter(player => !player.hand.find(card => card.name == 'moat'))
          .forEach(player => {
            player.deck.push(this.getCard('curse'));
            newState.log.push(`${player.name} gained: curse.`);
          });

        return newState;
      }
    },

    {
      name: 'militia',
      cost: 4,
      type: 'action',
      reducer: async (state: GameState) => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);

        const currentPlayer = state.players
          [state.turn % state.players.length];

        newState.players
          .filter(player => player.id != currentPlayer.id)
          .filter(player => !player.hand.find(card => card.name == 'moat'))
          .forEach(player => {
            // discard down to three cards
            while (player.hand.length > 3) {
                let index = Math.floor(Math.random() * player.hand.length);
                let card = player.hand.splice(index, 1)[0];
                player.discard.push(card);
                newState.log.push(`${player.name} was forced to discard: ${card.name}`);
            }
          });

          return newState;
      }
    },

    {
      name: 'moneylender',
      cost: 4,
      type: 'action',
      reducer: async (state: GameState) => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);

        const currentPlayer = state.players
          [state.turn % state.players.length];

        const card = currentPlayer.hand.find(card => card.name == 'copper');
        if (card) {
          const index = currentPlayer.hand.indexOf(card);
          currentPlayer.hand.splice(index, 1);
          currentPlayer.trash.push(card);
          currentPlayer.coins += 3;
        }

        return newState;
      }
    },

    {
      name: 'remodel',
      cost: 4,
      type: 'action',
      reducer: async (state: GameState) => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);

        const currentPlayer = state.players
          [state.turn % state.players.length];

        const card = currentPlayer.hand.find(card => card.name == 'copper');
        if (card) {
          const index = currentPlayer.hand.indexOf(card);
          currentPlayer.hand.splice(index, 1);
          currentPlayer.trash.push(card);
          currentPlayer.coins += 3;
        }

        return newState;
      }
    },


  ];

  /**
   * Returns an instance of the specified card
   * @param name
   */
  getCard(name: string) {
    return Object.assign({},
      this.cards.find(card => card.name === name)
    );
  }

  getInitialSupply(): Card[] {
    const cards = [];

    // 46 (60 - 14) coppers, 40 silvers, 30 golds
    for (let i = 0; i < (60 - 14); i ++) {
      cards.push(this.getCard('copper'));
      if (i < 40) cards.push(this.getCard('silver'));
      if (i < 30) cards.push(this.getCard('gold'));
    }

    // 8 victory cards of each type
    for (let i = 0; i < 8; i ++) {
      cards.push(this.getCard('estate'));
      cards.push(this.getCard('duchy'));
      cards.push(this.getCard('province'));
    }

    // 10 curse cards
    for (let i = 0; i < 10; i ++) {
      cards.push(this.getCard('curse'));
    }

    // use recommended starting cards
    const actionCards = [
     'cellar',
 //     'market',
      'militia',
//      'mine',
      'moat',
      'remodel',
//      'smithy',
      'village',
      'woodcutter',
      'workshop'
    ];

    // 10 of each action card
    actionCards.forEach(cardName => {
      for (let i = 0; i < 10; i ++) {
        cards.push(this.getCard(cardName));
      }
    })

    return cards;
  }

  /**
   * Selects a number of cards from the player's hand
   * (returns references to the cards)
   * @param player
   */
  async getSelection(player: Player, limit: number): Promise<Card[]> {
    const hand = player.hand;
    const selection = [];

    while (limit --) {
      let index = Math.floor(Math.random() * hand.length);
      selection.push(hand[index]);
    }

    return selection;
  }

  shuffle(list: any[]): any {
    const shuffled = [];

    while(list.length) {
      let index = Math.floor(Math.random() * list.length);
      shuffled.push(...list.splice(index, 1));
    }

    return shuffled;
  }
}
