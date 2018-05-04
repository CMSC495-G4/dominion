import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AudioService {

  muted: boolean = false;
  basePath = 'assets/sounds/';

  playLoop(filename: string) {
    const audio = this.playSound(filename);
    audio.loop = true;
    return audio;
  }

  playSound(filename: string) {
    let audio = new Audio(`${this.basePath}/${filename}`);
    if (!this.muted)
      audio.play();
    return audio;
  }

  setMuted(muted: boolean) {
    this.muted = muted;
  }
}
