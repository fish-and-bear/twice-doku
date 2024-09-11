import pygame.mixer
import asyncio

try:
    import js
    IS_WEB = True
except ImportError:
    IS_WEB = False

class AudioHandler:
    def __init__(self):
        self.sounds = {}
        self.volume = 0.5  # Default volume
        self.background_volume = 0.5  # Add this line for background music volume
        self.current_music = None

        if IS_WEB:
            js.eval('''
                window.audioContext = new (window.AudioContext || window.webkitAudioContext)();
                window.audioBuffers = {};
                window.loadSound = async function(url) {
                    const response = await fetch(url);
                    const arrayBuffer = await response.arrayBuffer();
                    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
                    window.audioBuffers[url] = audioBuffer;
                };
                window.playSound = function(url, loop, volume) {
                    const source = audioContext.createBufferSource();
                    source.buffer = window.audioBuffers[url];
                    source.loop = loop;
                    const gainNode = audioContext.createGain();
                    gainNode.gain.value = volume;
                    source.connect(gainNode).connect(audioContext.destination);
                    source.start();
                    return source;
                };
            ''')
        else:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)

    async def load_sound(self, path):
        try:
            if IS_WEB:
                await js.loadSound(path)
            else:
                sound = await asyncio.to_thread(pygame.mixer.Sound, path)
            self.sounds[path] = path if IS_WEB else sound
            return self.sounds[path]
        except Exception as e:
            print(f"Error loading sound {path}: {e}")
            return None

    def play(self, sound, loop=False, volume=None):
        if volume is None:
            volume = self.volume
        if IS_WEB:
            return js.playSound(sound, loop, volume)
        else:
            if isinstance(sound, pygame.mixer.Sound):
                sound.set_volume(volume)
                sound.play(loops=-1 if loop else 0)
            elif sound in self.sounds:
                self.sounds[sound].set_volume(volume)
                self.sounds[sound].play(loops=-1 if loop else 0)

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        if not IS_WEB:
            for sound in self.sounds.values():
                sound.set_volume(self.volume)

    def set_background_volume(self, volume):
        self.background_volume = max(0.0, min(1.0, volume))
        if not IS_WEB and self.current_music:
            pygame.mixer.music.set_volume(self.background_volume)

    def stop_all(self):
        if IS_WEB:
            js.eval('window.audioContext.suspend()')
        else:
            pygame.mixer.stop()
            pygame.mixer.music.stop()
        self.current_music = None

    def resume_all(self):
        if IS_WEB:
            js.eval('window.audioContext.resume()')
        else:
            pygame.mixer.unpause()

    def clear_all_queues(self):
        if IS_WEB:
            js.eval('window.audioContext.close()')  # Close the audio context to stop all sounds
            js.eval('window.audioContext = new (window.AudioContext || window.webkitAudioContext)();')  # Reinitialize
        else:
            pygame.mixer.stop()  # Stop all sounds in Pygame

    def is_playing(self, sound):
        if IS_WEB:
            # Implement web-based check if possible
            return False
        else:
            if pygame.mixer.music.get_busy():
                return True
            return False

    def play_music(self, music_file):
        if IS_WEB:
            # Implement web-based music playback if needed
            pass
        else:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)  # Loop indefinitely
            pygame.mixer.music.set_volume(self.background_volume)
        self.current_music = music_file

    def pause_music(self):
        if not IS_WEB:
            pygame.mixer.music.pause()

    def unpause_music(self):
        if not IS_WEB:
            pygame.mixer.music.unpause()

    def stop_music(self):
        if not IS_WEB:
            pygame.mixer.music.stop()
        self.current_music = None

    def set_music_end_event(self):
        if not IS_WEB:
            pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)

# ... other methods as needed ...