import { Injectable } from '@angular/core';
import { GameState, Card, Player } from '../models';
import { GameService } from '../game/game.service';
import { ServerService } from '../server/server.service';

@Injectable({
  providedIn: 'root'
})
export class CardsService {

  constructor(private server: ServerService) {

  }

  /** http://dominion.diehrstraits.com/?set=All&f=list */

  CARDS: Card[] = [
    {
      name: 'copper',
      cost: 0,
      type: 'treasure',
      value: 1,
      description: '+1 coin',
      soundFile: 'gold_or_province.mp3',
    },
    {
      name: 'silver',
      cost: 3,
      type: 'treasure',
      value: 2,
      description: '+2 coins',
      soundFile: 'gold_or_province.mp3',
    },
    {
      name: 'gold',
      cost: 6,
      type: 'treasure',
      value: 3,
      description: '+3 coins',
      soundFile: 'gold_or_province.mp3',
    },

    {
      name: 'estate',
      cost: 2,
      type: 'victory',
      value: 1,
      description: '+1 victory point',
      soundFile: 'gold_or_province.mp3',
    },
    {
      name: 'duchy',
      cost: 5,
      type: 'victory',
      value: 3,
      description: '+3 victory points',
      soundFile: 'gold_or_province.mp3',
    },
    {
      name: 'province',
      cost: 8,
      type: 'victory',
      value: 6,
      description: '+6 victory points',
      soundFile: 'gold_or_province.mp3',
    },

    {
      name: 'curse',
      cost: 0,
      type: 'curse',
      value: -1,
      description: '-1 victory point',
    },


    {
      name: 'cellar',
      cost: 2,
      type: 'action',
      description: 'Swap out your hand',
      soundFile: 'cellar.mp3',
      reducer: async (state: GameState)  => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);
        const currentPlayer = newState.players
          [state.turn % state.players.length];

        // allow the player to select all the cards in their hand
        const selection = await this.getRandomSelection(
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
      description: 'Trash up to four cards',
      soundFile: 'chapel.mp3',
      reducer: async (state: GameState) => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);
        const currentPlayer = newState.players
          [state.turn % state.players.length];

        // allow the player to select up to four cards
        const selection = await this.getRandomSelection(currentPlayer, 4);

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
      description: 'protect from attack',
      soundFile: 'moat.mp3',
      reducer: async (state: GameState)  => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);
        const currentPlayer = newState.players
          [state.turn % state.players.length];

          for (let i = 0; i < 2; i ++) {
            if (currentPlayer.deck.length == 0) {
              this.transfer(currentPlayer.discard, currentPlayer.deck, currentPlayer.discard.length)
              currentPlayer.deck = this.shuffle(currentPlayer.deck)
            }
            if (currentPlayer.deck.length > 0) {
              const card = currentPlayer.deck.pop();
              currentPlayer.hand.push(card);
            }
          }

        return newState;
      }
    },

    {
      name: 'chancellor',
      cost: 3,
      type: 'action',
      soundFile: 'throne_room_chancellor.mp3',
      description: '+2 coins, put your discard pile into your deck',
      reducer: async (state: GameState)  =>  {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);
        const currentPlayer = newState.players
          [state.turn % state.players.length];

        currentPlayer.coins += 2;

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
      name: 'woodcutter',
      cost: 3,
      type: 'action',
      description: '+1 buy, +2 coins',
      soundFile: 'remodel_workshop_smithy.mp3',
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
      name: 'merchant',
      cost: 3,
      type: 'action',
      description: '+1 cards, +1 action, +1 coin (w/ silver)',
      soundFile: 'buy.mp3',
      reducer: async (state: GameState) => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);

        const currentPlayer = state.players
          [state.turn % state.players.length];

        currentPlayer.actions += 1;
        if (currentPlayer.deck.length == 0) {
          this.transfer(currentPlayer.discard, currentPlayer.deck, currentPlayer.discard.length)
          currentPlayer.deck = this.shuffle(currentPlayer.deck)
        }
        if (currentPlayer.deck.length > 0) {
          this.transfer(currentPlayer.deck, currentPlayer.hand, 1);
        }
        if (currentPlayer.hand.find(card => card.name == 'silver'))
          currentPlayer.coins += 1;

        return newState;
      }
    },



    {
      name: 'vassal',
      cost: 3,
      type: 'action',
      description: 'discard top of deck. play discarded card if action',
      soundFile: 'remodel_workshop_smithy.mp3',
      reducer: async (state: GameState) =>  {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);
        const currentPlayer = newState.players
          [state.turn % state.players.length];

	const card = currentPlayer.deck.pop();
	if (card.type == 'action') {
	  currentPlayer.hand.push(card);
	  currentPlayer.actions += 1;
	}
	else {
	  currentPlayer.discard.push(card);
	}

        return newState;
      }
    },

    {
      name: 'village',
      cost: 3,
      type: 'action',
      soundFile: 'market_festival_village.mp3',
      description: '+1 card, +2 actions',
      reducer: async (state: GameState) =>  {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);
        const currentPlayer = newState.players
          [state.turn % state.players.length];

        // +1 card
        if (currentPlayer.deck.length == 0) {
          this.transfer(currentPlayer.discard, currentPlayer.deck, currentPlayer.discard.length)
          currentPlayer.deck = this.shuffle(currentPlayer.deck)
        }
        if (currentPlayer.deck.length > 0) {
          const card = currentPlayer.deck.pop();
          currentPlayer.hand.push(card);
        }
        
        const card = currentPlayer.deck.pop();
        currentPlayer.hand.push(card);

        // +2 actions
        currentPlayer.actions += 2;
        return newState;
      }
    },



    {
      name: 'workshop',
      cost: 3,
      type: 'action',
      description: '+4 coins, +1 buy',
      soundFile: 'remodel_workshop_smithy.mp3',
      reducer: async (state: GameState) =>  {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);
        const currentPlayer = newState.players
          [state.turn % state.players.length];

        // +4 coins
        currentPlayer.coins += 4;

        // +1 buys
        currentPlayer.buys += 1;

        return newState;
      }
    },


    {
      name: 'bureaucrat',
      cost: 4,
      type: 'action',
      description: 'gain a silver. opponents place victory card on top of deck',
      soundFile: 'militia.mp3',
      reducer: async (state: GameState) => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);

        const currentPlayer = state.players
          [state.turn % state.players.length];
	
	
        
        newState.players
          .filter(player => player.id != currentPlayer.id)
          .forEach(player => {
            if (player.hand.find(card => card.name == 'moat')) {
              this.server.sendLog(`${player.name}'s moat protects them!`);
            } else {
              const card = player.hand.find(card => card.type == 'victory');
              if (card) {
                const index = player.hand.indexOf(card);
                player.hand.splice(index, 1);
                player.deck.unshift(card);
              }
            }
          });

          return newState;
      }
    },

    {
      name: 'feast',
      cost: 4,
      type: 'action',
      description: '+5 coins, +1 buy, trash this card',
      soundFile: 'feast.mp3',
      reducer: async (state: GameState) => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);

        const currentPlayer = state.players
          [state.turn % state.players.length];

        const card = currentPlayer.discard.find(card => card.name == 'feast');
        if (card) {
          const index = currentPlayer.discard.indexOf(card);
          currentPlayer.discard.splice(index, 1);
          currentPlayer.trash.push(card);
        }
        
        currentPlayer.buys ++;
        currentPlayer.coins += 5;

        return newState;
      }
    },


    {
      name: 'gardens',
      cost: 4,
      type: 'victory',
      description: '+1 victory point/10 cards',
      soundFile: 'gardens.mp3',
    },

    {
      name: 'militia',
      cost: 4,
      type: 'action',
      description: 'opponents discard down to 3 cards',
      soundFile: 'militia.mp3',
      reducer: async (state: GameState) => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);

        const currentPlayer = state.players
          [state.turn % state.players.length];

        currentPlayer.coins += 2;
        
        newState.players
          .filter(player => player.id != currentPlayer.id)
          .forEach(player => {
            if (player.hand.find(card => card.name == 'moat')) {
              this.server.sendLog(`${player.name}'s moat protects them!`);
            } else {
              // discard down to three cards
              while (player.hand.length > 3) {
                let index = Math.floor(Math.random() * player.hand.length);
                let card = player.hand.splice(index, 1)[0];
                this.server.sendLog(`${player.name} is forced to discard a${/aeiou/i.test(card.name) ? 'n' : ''} ${card.name}!`);
                player.discard.push(card);
              }
            }
          });

          return newState;
      }
    },

    {
      name: 'moneylender',
      cost: 4,
      type: 'action',
      description: 'trash a copper for +3 coins',
      soundFile: 'moneylender.mp3',
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
      name: 'poacher',
      cost: 4,
      type: 'action',
      description: 'trash a copper for +3 coins',

      reducer: async (state: GameState) => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);

        const currentPlayer = state.players
          [state.turn % state.players.length];

	currentPlayer.actions += 1;
	currentPlayer.coins += 1;

	if (currentPlayer.deck.length == 0) {
          this.transfer(currentPlayer.discard, currentPlayer.deck, currentPlayer.discard.length)
          currentPlayer.deck = this.shuffle(currentPlayer.deck)
        }
        if (currentPlayer.deck.length > 0) {
          this.transfer(currentPlayer.deck, currentPlayer.hand, 1);
        }

        return newState;
      }
    },

    {
      name: 'remodel',
      cost: 4,
      type: 'action',
      description: 'trash a copper for +3 coins',

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
      name: 'smithy',
      cost: 4,
      type: 'action',
      description: '+3 cards',
      soundFile: 'remodel_workshop_smithy.mp3',
      reducer: async (state: GameState) => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);

        const currentPlayer = state.players
          [state.turn % state.players.length];
        
        for (let i = 0; i < 3; i++) {
          if (currentPlayer.deck.length == 0) {
            this.transfer(currentPlayer.discard, currentPlayer.deck, currentPlayer.discard.length)
            currentPlayer.deck = this.shuffle(currentPlayer.deck)
          }
          if (currentPlayer.deck.length > 0) {
            this.transfer(currentPlayer.deck, currentPlayer.hand, 1);
          }
        }
        return newState;
      }
    },

    {
      name: 'throne room',
      cost: 4,
      type: 'action',
      description: 'play an action card twice',
      soundFile: 'remodel_workshop_smithy.mp3',
      reducer: async (state: GameState) => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);

        const currentPlayer = state.players
          [state.turn % state.players.length];
        
        
        
        return newState;
      }
    },

    {
      name: 'bandit',
      cost: 5,
      type: 'action',
      description: 'gain a gold. opponents discard top two cards from deck. trash a silver or gold',
      soundFile: 'militia.mp3',
      reducer: async (state: GameState) => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);

        const currentPlayer = state.players
          [state.turn % state.players.length];

        currentPlayer.coins += 2;
        
        newState.players
          .filter(player => player.id != currentPlayer.id)
          .forEach(player => {
            if (player.hand.find(card => card.name == 'moat')) {
              this.server.sendLog(`${player.name}'s moat protects them!`);
	    } 
	    else {
              
            }
          });

          return newState;
      }
    },

    {
      name: 'council room',
      cost: 5,
      type: 'action',
      description: '+4 cards, +1 buy, other players draw a card',
      soundFile: 'throne_room_chancellor.mp3',
      reducer: async (state: GameState) => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);

        const currentPlayer = state.players
          [state.turn % state.players.length];

        for (let i = 0; i < 4; i++) {
          if (currentPlayer.deck.length == 0) {
            this.transfer(currentPlayer.discard, currentPlayer.deck, currentPlayer.discard.length)
            currentPlayer.deck = this.shuffle(currentPlayer.deck)
          }
          if (currentPlayer.deck.length > 0) {
            this.transfer(currentPlayer.deck, currentPlayer.hand, 1);
          }
        }
        
        currentPlayer.buys ++;

        newState.players
          .filter(player => player.id != currentPlayer.id)
          .forEach(player => {
            this.transfer(player.deck, player.hand, 1);
          });

        return newState;
      }
    },



    {
      name: 'festival',
      cost: 5,
      type: 'action',
      description: '+2 actions, +1 buy, +2 coins',
      soundFile: 'market_festival_village.mp3',
      reducer: async (state: GameState) => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);

        const currentPlayer = state.players
          [state.turn % state.players.length];

        currentPlayer.actions += 2;
        currentPlayer.buys ++;
        currentPlayer.coins += 2;

        return newState;
      }
    },


    {
      name: 'laboratory',
      cost: 5,
      type: 'action',
      description: '+2 cards, +1 action',
      soundFile: 'lab_witch.mp3',

      reducer: async (state: GameState) => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);

        const currentPlayer = state.players
          [state.turn % state.players.length];

        currentPlayer.actions += 1;
        for (let i = 0; i < 2; i++) {
          if (currentPlayer.deck.length == 0) {
            this.transfer(currentPlayer.discard, currentPlayer.deck, currentPlayer.discard.length)
            currentPlayer.deck = this.shuffle(currentPlayer.deck)
          }
          if (currentPlayer.deck.length > 0) {
            this.transfer(currentPlayer.deck, currentPlayer.hand, 1);
          }
        }
        return newState;
      }
    },

    {
      name: 'library',
      cost: 5,
      type: 'action',
      description: 'draw until hand has seven cards. can set aside any action cards drawn',
      soundFile: 'lab_witch.mp3',

      reducer: async (state: GameState) => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);

        const currentPlayer = state.players
          [state.turn % state.players.length];

	while(currentPlayer.hand.length < 7) {
          if (currentPlayer.deck.length == 0) {
            this.transfer(currentPlayer.discard, currentPlayer.deck, currentPlayer.discard.length)
            currentPlayer.deck = this.shuffle(currentPlayer.deck)
          }
          if (currentPlayer.deck.length > 0) {
            this.transfer(currentPlayer.deck, currentPlayer.hand, 1);
          }
        }
        return newState;
      }
    },

    {
      name: 'market',
      cost: 5,
      type: 'action',
      description: '+1 cards, +1 action, +1 buy, +1 coin',
      soundFile: 'market_festival_village.mp3',
      reducer: async (state: GameState) => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);

        const currentPlayer = state.players
          [state.turn % state.players.length];

        currentPlayer.actions += 1;
        currentPlayer.buys += 1;
        currentPlayer.coins += 1;
        if (currentPlayer.deck.length == 0) {
          this.transfer(currentPlayer.discard, currentPlayer.deck, currentPlayer.discard.length)
          currentPlayer.deck = this.shuffle(currentPlayer.deck)
        }
        if (currentPlayer.deck.length > 0) {
          this.transfer(currentPlayer.deck, currentPlayer.hand, 1);
        }

        return newState;
      }
    },

    {
      name: 'mine',
      cost: 5,
      type: 'action',
      description: 'silver to gold, or copper to silver',
      soundFile: 'buy.mp3',
      reducer: async (state: GameState) => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);

        const currentPlayer = state.players
          [state.turn % state.players.length];

        const silver = currentPlayer.hand.find(card => card.name == 'silver');
        const copper = currentPlayer.hand.find(card => card.name == 'copper');

        if (silver) {
          let silverIndex = currentPlayer.hand.indexOf(silver);
          currentPlayer.trash.push(...currentPlayer.hand.splice(silverIndex, 1));
          currentPlayer.hand.push(this.getCard('gold'));

        } else if (copper) {
          let copperIndex = currentPlayer.hand.indexOf(copper);
          currentPlayer.trash.push(...currentPlayer.hand.splice(copperIndex, 1));
          currentPlayer.hand.push(this.getCard('silver'));
        }

        return newState;
      }
    },


    {
      name: 'witch',
      cost: 5,
      type: 'action',
      description: 'opponents gain a curse',
      soundFile: 'lab_witch.mp3',
      reducer: async (state: GameState) => {
        const { id, players, winner, turn, phase, supply } = state;
        const newState = Object.assign({}, state);
        const currentPlayer = newState.players
          [state.turn % state.players.length];

        for (let i = 0; i < 2; i ++) {
          if (currentPlayer.deck.length == 0) {
              this.transfer(currentPlayer.discard, currentPlayer.deck, currentPlayer.discard.length)
              currentPlayer.deck = this.shuffle(currentPlayer.deck)
            }
          if (currentPlayer.deck.length > 0) {
            const card = currentPlayer.deck.pop();
            currentPlayer.hand.push(card);
          }
        }

        newState.players
          .filter(player => player.id != currentPlayer.id)
          .forEach(player => {
            if (player.hand.find(card => card.name == 'moat')) {
              this.server.sendLog(`${player.name}'s moat protects them!`);
            } else {
              this.server.sendLog(`${player.name} has been cursed!`);
              player.hand.push(this.getCard('curse'));
            }
          });

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
      this.CARDS.find(card => card.name === name)
    );
  }

  getInitialDeck(): Card[] {
    const cards = [];

    for (let i = 0; i < 7; i ++) {
      cards.push(this.getCard('copper'));
    }

    for (let j = 0; j < 3; j ++) {
      cards.push(this.getCard('estate'));
    }

    return cards;
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
//     'cellar',
      'market',
      'feast',

      'militia',
      'mine',
      'moat',
      'chancellor',
      'council room',
      'festival',
      'gardens',
      'laboratory',
      'merchant',

//      'remodel',
      'smithy',
      'moneylender',
      'village',
      'woodcutter',
      'witch',
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
  async getRandomSelection(player: Player, limit: number): Promise<Card[]> {
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

  transfer(from: any[], to: any[], count: number) {
    while (count-- && from.length) {
      to.push(from.pop())
    }
  }

  getVictoryScore(cards: Card[]): number {
    return cards
      .filter(card => ['victory', 'curse'].includes(card.type))
      .reduce((prev, curr) => {
        let value = curr.value;
        if (curr.name == 'gardens')
          value = Math.floor(cards.length / 10);
        return prev += value
      }, 0);
  }
}
