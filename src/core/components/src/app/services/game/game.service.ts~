import { Injectable } from '@angular/core';
import { Card, GameState, Player } from '../models';
import { CardsService } from '../cards/cards.service';
import { ServerService } from '../server/server.service';
import { AudioService } from '../audio/audio.service';

@Injectable({
  providedIn: 'root'
})
export class GameService {

  config: any = window['config'];

  playerInfo: {
    id: number;
    name: string;
  } = this.config.player;

  state: GameState = {
    id: this.config.gameId,
    players: [],
    winner: null,
    turn: 0,
    phase: 'action',
    supply: [],
  };

  constructor(
    private cards: CardsService,
    private server: ServerService,
    private audio: AudioService) {

    this.state.supply = this.cards.getInitialSupply();

    let players: Player[] = [];
    let playerConfigs: any[] = this.config.players;

    for (let config of playerConfigs) {
      let player: Player = {
        id: +config.id,
        name: config.name,

        deck: cards.getInitialDeck(),
        hand: [],
        selection: [],
        discard: [],
        trash: [],
        coins: 0,
        actions: 1,
        buys: 1,
      }

      cards.transfer(player.deck, player.hand, 5);
      this.state.players.push(player);
    }

    this.server.updateEvents
      .subscribe(update => {
        if (update.turn != this.state.turn) {
          this.audio.playSound('action.mp3');
        }
        this.state = update;
      });
  }

  startTurn() {


  }

  buyCard(card: Card) {
    const player = this.getCurrentPlayer();

    if (this.canBuyCard(card)) {
      let index = this.state.supply.indexOf(card);
      let supplyCard = this.state.supply.splice(index, 1)[0];
      player.discard.push(supplyCard);
      player.buys --;
      player.coins -= card.cost;
      this.server.sendUpdate(this.state);
      this.server.sendLog(`${player.name} buys a${/[aeiou]/i.test(card.name[0]) ? 'n' : ''} ${card.name}!`)
      if (card.soundFile) {
        this.audio.playSound(card.soundFile);
      }
      this.checkVictory();
    } else {
      console.log(`Can't buy`, card, player);
    }
  }

  canBuyCard(card: Card) {
    const player = this.getCurrentPlayer();

    return this.isPlayersTurn()
      && this.state.phase == 'buy'
      && player.buys > 0
      && card.cost <= player.coins;
  }

  async playCard(card: Card) {
    const player = this.getCurrentPlayer();

    if (this.isPlayersTurn()
      && this.state.phase == 'action'
      && card.type == 'action'
      && player.actions > 0) {
      this.server.sendLog(`${player.name} plays a${/[aeiou]/i.test(card.name[0]) ? 'n' : ''} ${card.name}!`)
      player.actions --;
      const reducer = this.getCardReducer(card.name);
      this.state = await reducer(this.state);

      let handIndex = player.hand.indexOf(card);
      player.discard.push(...player.hand.splice(handIndex, 1));

      if (card.soundFile) {
        this.audio.playSound(card.soundFile);
      }

      this.server.sendUpdate(this.state);
    } else {
      console.log('It is not the correct time to play that card.');
    }
  }

  endActions() {
    const player = this.getCurrentPlayer();
    this.state.phase = 'buy';
    player.coins += this.calculateCoins()
    this.audio.playSound('buy.mp3');


    this.server.sendUpdate(this.state);
    this.server.sendLog(`${this.getPlayer().name} has finished their actions.`);
  }

  endTurn() {
    this.audio.playSound('cleanup.mp3');
    const player = this.getCurrentPlayer();

    this.state.turn ++;
    this.state.phase = 'action';
    this.cards.transfer(player.hand, player.discard, player.hand.length);

    if (player.deck.length < 5) {
      this.cards.transfer(player.discard, player.deck, player.discard.length);
      player.deck = this.cards.shuffle(player.deck);
    }

    this.cards.transfer(player.deck, player.hand, 5);
    player.actions = 1;
    player.buys = 1;
    player.coins = 0;

    this.server.sendLog(`${this.getPlayer().name} has ended their turn.`);
    this.server.sendUpdate(this.state);
  }

  getNextPhase(phase: string): string {
    switch(phase) {
      case 'action':
        return 'buy';

      case 'buy':
        return 'cleanup';

      case 'cleanup':
      default:
        return 'action';
    }
  }

  isGameOver() {
    return this.state.supply
      .filter(card => card.name == 'province')
      .length == 0;
  }

  checkVictory() {
    if (this.isGameOver()) {
      this.state.winner = this.getWinner();
      this.audio.playSound('game_won.mp3');
    }
  }

  getWinner() {
    return this.state.players.reduce((prev, curr) => {
      let prevScore = this.cards.getVictoryScore([
        ...prev.deck,
        ...prev.hand,
        ...prev.discard
      ]);
      let currScore = this.cards.getVictoryScore([
        ...curr.deck,
        ...curr.hand,
        ...curr.discard
      ]);
      return prevScore > currScore
        ? prev
        : curr;
    })
  }

  calculateCoins() {
    const player = this.getPlayer();
    return player.hand
      .filter(card => card.type == 'treasure')
      .reduce((prev, curr) => prev + curr.value, 0);
  }

  isPlayersTurn() {
    return this.getPlayer() == this.getCurrentPlayer();
  }

  getPlayer(): Player {
    return this.state.players
      .find(player => player.id == this.playerInfo.id);
  }

  getOpponent(): Player {
    return this.state.players
      .find(player => player.id != this.playerInfo.id);
  }

  getCurrentPlayer(): Player {
    const { players, turn } = this.state;
    return players[turn % players.length];
  }

  getOpponentName() {
    return this.getOpponent().name;
  }

  getOpponentVictoryScore () {
    const player = this.getOpponent();
    const deck = [
      ...player.deck,
      ...player.hand,
      ...player.discard
    ];
    return this.cards.getVictoryScore(deck);
  }

  getVictoryScore() {
    const player = this.getPlayer();
    const deck = [
      ...player.deck,
      ...player.hand,
      ...player.discard
    ];
    return this.cards.getVictoryScore(deck);
  }

  getCardReducer(cardName: string) {
    return this.cards.CARDS.find(card => card.name == cardName).reducer;
  }

}
