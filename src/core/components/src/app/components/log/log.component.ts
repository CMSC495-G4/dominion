import { Component, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { ServerService } from '../../services/server/server.service';

@Component({
  selector: 'app-log',
  templateUrl: './log.component.html',
  styleUrls: ['./log.component.css']
})
export class LogComponent implements AfterViewInit {

  @ViewChild('log')
  logPane: ElementRef;

  messages = [];

  constructor(private server: ServerService) {}

  ngAfterViewInit() {
    let el = this.logPane.nativeElement as HTMLElement;

    this.server.logEvents.subscribe(message => {
      this.messages.push(message);
      setTimeout(() => {
        el.scrollTop = el.scrollHeight;
      }, 0);
    });
  }
}
