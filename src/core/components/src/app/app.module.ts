import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { SupplyComponent } from './components/supply/supply.component';
import { ChatComponent } from './components/chat/chat.component';
import { LogComponent } from './components/log/log.component';

import { CardsService } from './services/cards/cards.service';
import { ServerService } from './services/server/server.service';

import { HandComponent } from './components/hand/hand.component';
import { StatusComponent } from './components/status/status.component'


@NgModule({
  declarations: [
    AppComponent,
    SupplyComponent,
    ChatComponent,
    LogComponent,
    HandComponent,
    StatusComponent
  ],
  imports: [
    BrowserModule,
  ],
  providers: [
    CardsService,
    ServerService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
