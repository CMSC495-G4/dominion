import { Injectable } from '@angular/core';
import { Card, GameState, Player } from '../models';
import { CardsService } from '../cards/cards.service';
import { ServerService } from '../server/server.service';

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
    private server: ServerService) {

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
      .subscribe(update => this.state = update);
  }

  startTurn() {

  }

  endActions() {
    this.state.phase = 'buy';
    this.server.sendUpdate(this.state);
    this.server.sendLog(`${this.getPlayer().name} has finished their actions.`);
  }

  endTurn() {
    this.state.turn ++;
    this.state.phase = 'action';
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

}
