import { Component } from '@angular/core';
import { ServerService } from '../../services/server/server.service';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent {

  messages = '';

  constructor(private server: ServerService) {
    server.chatEvents.subscribe(message => {
      this.messages += message + '\n';
    })
  }

  handleKeyUp(event: KeyboardEvent) {
    const element = event.target as HTMLInputElement;

    if (event.code == 'Enter') {
      let message = element.value;
      this.server.sendChat(message);
      element.value = '';
    }
  }
}
