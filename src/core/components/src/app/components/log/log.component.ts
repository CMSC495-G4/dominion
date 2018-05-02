import { Component } from '@angular/core';
import { ServerService } from '../../services/server/server.service';

@Component({
  selector: 'app-log',
  templateUrl: './log.component.html',
  styleUrls: ['./log.component.css']
})
export class LogComponent {

  messages = '';

  constructor(private server: ServerService) {
    server.logEvents.subscribe(message => {
      this.messages += message + '\n\n';
    });
  }
}
