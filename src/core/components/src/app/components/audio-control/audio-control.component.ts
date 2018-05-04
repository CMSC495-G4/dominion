import { Component, AfterViewInit } from '@angular/core';
import { AudioService } from '../../services/audio/audio.service';

@Component({
  selector: 'app-audio-control',
  templateUrl: './audio-control.component.html',
  styleUrls: ['./audio-control.component.css']
})
export class AudioControlComponent implements AfterViewInit {

  muted = false;
  backgroundTracks = [
    'background_1.mp3',
    'background_2.mp3',
  ];
  lastPlayed = Math.floor(Math.random() * 2);
  audioElement: HTMLAudioElement;
  gameStart: HTMLAudioElement;

  constructor(private audio: AudioService) {}

  ngAfterViewInit() {
    this.gameStart = this.audio.playSound('game_start.mp3');
    this.gameStart.volume = 0.7;
    this.gameStart.addEventListener('ended', () => {
      this.audioElement = this.audio.playLoop(
        this.backgroundTracks[this.lastPlayed]
      );
      this.audioElement.volume = 0.6;
    })
  }

  toggleAudio() {
    this.muted = !this.muted;
    this.audio.setMuted(this.muted);
    if (this.muted) {
      this.audioElement && this.audioElement.pause();
    } else {
      this.audioElement && this.audioElement.play();
    }
  }

}
