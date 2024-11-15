import audiobusio
import audiocore
import board
import array
import time
import math

print(dir(board))
# Generate one period of sine wave.
length = 8000 // 440
sine_wave = array.array("H", [0] * length)
for i in range(length):
    sine_wave[i] = int(math.sin(math.pi * 2 * i / length) * (2 ** 15) + 2 ** 15)

sine_wave = audiocore.RawSample(sine_wave, sample_rate=8000)
# i2s = audiobusio.I2SOut(board.I2S_BCK, board.I2S_WS, board.I2S_DOUT)
i2s = audiobusio.I2SOut(board.SPEAKER_SCK, board.SPEAKER_WS, board.SPEAKER_DOUT)
i2s.play(sine_wave, loop=True)
time.sleep(1)
i2s.stop()

