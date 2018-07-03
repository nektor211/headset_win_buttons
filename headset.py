
# coding: utf-8

# In[ ]:


import sounddevice as sd
import win32api
import win32con
from time import sleep
import numpy as np


SAMPLE_RATE = 1000 # Sample rate for our input stream
BLOCK_SIZE = 250# Number of samples before we trigger a processing callback

SUPPRESS_SECONDS = 2

SUPPRESS_BLOCKS = (SUPPRESS_SECONDS * SUPPRESS_SECONDS) // BLOCK_SIZE

# TODO handle +/- buttons too by processing several blocks and properly detecting peaks


VK_MEDIA_PLAY_PAUSE = 0xB3

def toggle_play():
    win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, 0, 0, 0)

class HeadsetButtonController:
    times_pressed = 0
    suppress = 0

    def process_frames(self, indata, frames, time, status):
        if self.suppress:
            self.suppress -= 1
        max_ = np.max(indata)

        if max_ > 0.8:
            # The button was pressed!
            print('toggle_play')
            toggle_play()
            self.suppress = SUPPRESS_BLOCKS

    def __init__(self):
        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            blocksize=BLOCK_SIZE,
            channels=1,
            callback=self.process_frames
        )
        self.stream.start()

if __name__ == '__main__':
    controller = HeadsetButtonController()

    try:
        while True:
            sleep(10)
    except:
        controller.stream.stop()

