export interface GameState {
    id: number;
    players: Player[];
    winner: Player;
    turn: number;
    phase: "action" | "buy" | "cleanup";
    supply: Card[];
    log?: string[];
}

export interface Player {
    id: number;
    name: string;
    deck: Card[];
    hand: Card[];
    selection: Card[];
    discard: Card[];
    trash: Card[];
    coins: number;
    actions: number;
    buys: number;
}

export interface Card {
    name: string;
    type: "action" | "reaction" | "treasure" | "victory" | "curse";
    cost: number;
    value?: number;
    reducer?: (GameState) => Promise<GameState>;
}

export interface Message {
    user: string;
    text: string;
}