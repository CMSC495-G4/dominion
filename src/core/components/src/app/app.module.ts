import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { SupplyComponent } from './components/supply/supply.component';
import { ChatComponent } from './components/chat/chat.component';
import { LogComponent } from './components/log/log.component';

import { CardsService } from './services/cards/cards.service';
import { ServerService } from './services/server/server.service';
import { GameService } from './services/game/game.service';
import { AudioService } from './services/audio/audio.service';

import { HandComponent } from './components/hand/hand.component';
import { StatusComponent } from './components/status/status.component';
import { CardComponent } from './components/card/card.component';
import { AudioControlComponent } from './components/audio-control/audio-control.component'


@NgModule({
  declarations: [
    AppComponent,
    SupplyComponent,
    ChatComponent,
    LogComponent,
    HandComponent,
    StatusComponent,
    CardComponent,
    AudioControlComponent
  ],
  imports: [
    BrowserModule,
  ],
  providers: [
    CardsService,
    ServerService,
    GameService,
    AudioService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
