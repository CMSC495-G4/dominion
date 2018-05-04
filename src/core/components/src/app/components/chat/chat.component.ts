import { Component, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import { ServerService } from '../../services/server/server.service';
import { Message } from '../../services/models';
import { AudioService } from '../../services/audio/audio.service';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css']
})
export class ChatComponent implements AfterViewInit {

  @ViewChild('pane')
  chatPane: ElementRef;

  @ViewChild('input')
  chatInput: ElementRef;

  messages: Message[] = [];

  constructor(private server: ServerService, private audio: AudioService) {}

  ngAfterViewInit() {

    this.server.chatEvents.subscribe(message => {
      this.messages.push(message);

      if (document.activeElement != this.chatInput.nativeElement) {
        this.audio.playSound('chat.mp3')
      }

      setTimeout(() => {
        let el = this.chatPane.nativeElement as Element;
        el.scrollTop = el.scrollHeight - el.clientHeight;
      }, 0);
    })
  }


  handleKeyUp(event: KeyboardEvent) {
    const element = event.target as HTMLInputElement;

    if (event.code == 'Enter') {
      this.server.sendChat({
        user: window['config'].player.name,
        text: element.value
      })
      element.value = '';
    }
  }
}
