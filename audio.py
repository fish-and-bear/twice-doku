import pygame.mixer

class AudioHandler:
    BACKGROUND = 0
    SFX = 1

    def __init__(self, maxBackground=1, maxSfx=4):
        self.background = []
        self.backgroundQueue = []
        self.sfx = []
        self.sfxQueue = []

        self.maxBackground = maxBackground
        self.maxSfx = maxSfx

        self.backgroundVolume = 1
        self.sfxVolume = 1

        self.index = 0

    def pre_init(self, frequency=44100, size=-16, channels=2, buffer=2**9, devicename=None):
        pygame.mixer.pre_init(frequency, size, channels, buffer, devicename)

    def init(self):
        pygame.mixer.init()

        maxChannels = pygame.mixer.get_num_channels()

        while self.maxBackground+self.maxSfx > maxChannels:
            if self.maxSfx > 1:
                self.maxSfx -= 1
            elif self.maxBackground > 1:
                self.maxBackground -= 1

    def play_background(self, music, queue=True, loops=0, maxtime=0):
        if music is not None:
            if self.all_busy(self.background):
                if len(self.background) < self.maxBackground:
                    newChannel = pygame.mixer.Channel(self.index)
                    newChannel.set_volume(self.backgroundVolume)
                    self.background.append(newChannel)
                    self.index += 1
                    c = self.get_free(self.background)
                    #c.play(music, loops=loops, maxtime=maxtime)
                    #c.set_volume(self.backgroundVolume) # volume resets when new music is loaded

                else:
                    if queue:
                        self.backgroundQueue.append([music,loops,maxtime])
            else:
                c = self.get_free(self.background)
                c.play(music, loops=loops, maxtime=maxtime)
                c.set_volume(self.backgroundVolume) # volume resets when new music is loaded

    def play_sfx(self, sfx, queue=False, loops=0, maxtime=0):
        if sfx is not None:
            if self.all_busy(self.sfx):
                if len(self.sfx) < self.maxSfx:
                    newChannel = pygame.mixer.Channel(self.index)
                    newChannel.set_volume(self.sfxVolume)
                    self.sfx.append(newChannel)
                    self.index += 1
                    c = self.get_free(self.sfx)
                    c.play(sfx, loops=loops, maxtime=maxtime)
                    c.set_volume(self.sfxVolume) # volume resets when new music is loaded

                else:
                    if queue:
                        self.sfxQueue.append([sfx,loops,maxtime])
            else:
                c = self.get_free(self.sfx)
                c.play(sfx, loops=loops, maxtime=maxtime)
                c.set_volume(self.sfxVolume) # volume resets when new music is loaded

    def play(self, sound, channel=None, queue=True, loops=0, maxtime=0):
        if channel is None:
            channel = AudioHandler.SFX
            
        if channel == AudioHandler.SFX:
            self.play_sfx(sound, queue, loops, maxtime)
        elif channel == AudioHandler.BACKGROUND:
            self.play_background(sound, queue, loops, maxtime)
        else:
            raise self.InvalidChanneLGroupError('Specified channel group does not exist!')

    def queue_background(self, music, loops=0, maxtime=0):
        self.backgroundQueue.append([music,loops,maxtime])

    def queue_sfx(self, sfx, loops=0, maxtime=0):
        self.sfxQueue.append([sfx,loops,maxtime])
    
    def queue(self, sound, channel=None, loops=0, maxtime=0):
        if channel is None:
            channel = AudioHandler.SFX

        if channel == AudioHandler.SFX:
            self.queue_sfx(sound, loops, maxtime)
        elif channel == AudioHandler.BACKGROUND:
            self.queue_background(sound, loops, maxtime)
        else:
            raise self.InvalidChanneLGroupError('Specified channel group does not exist!')

    def clear_queue(self, channel=None):
        if channel is None:
            channel = AudioHandler.SFX

        if channel == AudioHandler.SFX:
            self.sfxQueue = []
        elif channel == AudioHandler.BACKGROUND:
            self.backgroundQueue = []
        else:
            raise self.InvalidChanneLGroupError('Specified channel group does not exist!')

    def clear_all_queues(self):
        for channel in [AudioHandler.SFX, AudioHandler.BACKGROUND]: # if more channel types added, update this list
            self.clear_queue(channel)

    def stop_channel(self, channel=None):
        if channel == AudioHandler.SFX:
            for channel in self.sfx:
                channel.stop()
        elif channel == AudioHandler.BACKGROUND:
            for channel in self.background:
                channel.stop()
        else:
            raise self.InvalidChanneLGroupError('Specified channel group does not exist!')

    def stop_all(self):
        for channel in [AudioHandler.SFX, AudioHandler.BACKGROUND]: # if more channel types added, update this list
            self.stop_channel(channel)

    def fadeout_channel(self, channel=None, time=0):
        if channel == AudioHandler.SFX:
            for channel in self.sfx:
                channel.fadeout(time)
        elif channel == AudioHandler.BACKGROUND:
            for channel in self.background:
                channel.fadeout(time)
        else:
            raise self.InvalidChanneLGroupError('Specified channel group does not exist!')

    def fadeout_all(self, time=0):
        for channel in [AudioHandler.SFX, AudioHandler.BACKGROUND]: # if more channel types added, update this list
            self.fadeout_channel(channel, time)

    def set_channel_volume(self, channel=None, volume=1):
        if channel == AudioHandler.SFX:
            self.sfxVolume = volume
            for channel in self.sfx:
                channel.set_volume(volume)

        elif channel == AudioHandler.BACKGROUND:
            self.backgroundVolume = volume
            for channel in self.background:
                channel.set_volume(volume)

        else:
            raise self.InvalidChanneLGroupError('Specified channel group does not exist!')

    def set_all_volume(self, volume=1):
        for channel in [AudioHandler.SFX, AudioHandler.BACKGROUND]: # if more channel types added, update this list
            self.set_channel_volume(channel, volume)

    def all_busy(self, group):
        for channel in group:
            if not channel.get_busy():
                return False
        return True

    def get_free(self, group):
        for channel in group:
            if not channel.get_busy():
                return channel
        return None

    def refresh(self):
        for music in self.backgroundQueue:
            if self.all_busy(self.background) and len(self.background) >= self.maxBackground:
                break
            else:
                self.play_background(music[0], queue=False, loops=music[1], maxtime=music[2])
                self.backgroundQueue.remove(music)

        for sfx in self.sfxQueue:
            if self.all_busy(self.sfx) and len(self.sfx) >= self.maxSfx:
                break
            else:
                self.play_sfx(sfx[0], queue=False, loops=sfx[1], maxtime=sfx[2])
                self.sfxQueue.remove(sfx)
    
    class InvalidChanneLGroupError(Exception):
        pass
