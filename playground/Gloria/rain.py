import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import get_data as aub
from scale import listscale, rgbscale
from wavlength import wavlength
import pyaudio, wave
import atexit, random, time, math, sys
import mutagen.wavpack

# Audio

if len(sys.argv) < 2:
    print("Usage: python3 rain.py file.wav")
    raise OSError

PATH = sys.argv[1]
pA = pyaudio.PyAudio()
wav = wave.open(PATH)
stream = pA.open(format =
                pA.get_format_from_width(wav.getsampwidth()),
                channels = wav.getnchannels(),
                rate = wav.getframerate(),
                output = True)
chunk = 2048
data = wav.readframes(chunk)

# Constant declarations

INTERVAL = 15
DROP_COUNT = 50
FILELENGTH = (wavlength(PATH))

# Variable to control the pitch up and down
PITCH_LIST = aub.get_pitch(PATH)
TEMPO_LIST = aub.get_tempo(PATH)
VOLUME = listscale(aub.get_volume(PATH))
print(len(PITCH_LIST))
print(len(VOLUME))
print(TEMPO_LIST)

## CONSTANTS
VOLUME_SCALING = 0.8
PITCH_SCALED = listscale(PITCH_LIST)
TEMPO_SCALED = listscale(TEMPO_LIST)
print(len(TEMPO_LIST), len(PITCH_LIST))
PITCH_TIME_RATIO = len(PITCH_LIST) / FILELENGTH
VOLUME_TIME_RATIO = len(VOLUME) / FILELENGTH

# Creates a figurue and removes the toolbar.
plt.rcParams['toolbar'] = 'None'
fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0, 1), ax.set_xticks([])
ax.set_ylim(0, 1), ax.set_yticks([])


# Create rain data

rain_drops = np.zeros(DROP_COUNT, dtype=[('position', float, 2),
                                      ('size',     float, 1),
                                      ('growth',   float, 1),
                                      ('color',    float, 4)])

# Initialize the raindrops in random positions and with
# random growth rates.
rain_drops['position'] = np.random.uniform(0.25, 0.50, (DROP_COUNT, 2))
rain_drops['growth'] = np.random.uniform(50, 200, DROP_COUNT)

# Construct the scatter which we will update during animation
# as the raindrops develop.
scat = ax.scatter(rain_drops['position'][:, 0], rain_drops['position'][:, 1],
                  s=1, lw=0.5, edgecolors='none',
                  facecolors=rain_drops['color'])
T0 = time.time()
print(PITCH_TIME_RATIO)

def update(frame_number):
    time_position = math.floor((time.time() - T0) * PITCH_TIME_RATIO)
    volume_position = math.floor((time.time() - T0) * VOLUME_TIME_RATIO)
    if time_position >= len(PITCH_LIST):
        return
    # Get an index which we can use to re-spawn the oldest raindrop.
    current_index = frame_number % DROP_COUNT

    # Make all colors more transparent as time progresses.
    rain_drops['color'][:, 3] -= 1.0/len(rain_drops)
    rain_drops['color'][:, 3] = np.clip(rain_drops['color'][:, 3], 0, 1)

    # Make all circles bigger.
    rain_drops['size'] += rain_drops['growth']

    r = PITCH_SCALED[time_position-1]
    
    rain_drops['position'][current_index, 0] = np.random.uniform(0, 1, 1)
    rain_drops['position'][current_index, 1] = np.random.uniform(0.5-VOLUME[volume_position] * VOLUME_SCALING, 0.5+VOLUME[volume_position] * VOLUME_SCALING, 1)
    rain_drops['size'][current_index] = 10
    rain_drops['color'][current_index] = (r, 0, 0, 1)
    rain_drops['growth'][current_index] = np.random.uniform(50, 200)

    # update scatter plot data
    scat.set_facecolors(rain_drops['color'])
    scat.set_sizes(rain_drops['size'])
    scat.set_offsets(rain_drops['position'])

    # Write chunk of audio into the output
    global data
    global stream
    stream.write(data)
    data = wav.readframes(chunk) 

# Construct the animation, using the update function as the animation director.
animation = FuncAnimation(fig, update, interval=INTERVAL)
fig.patch.set_facecolor((0.8, 0.9, 0.8))
#fig.canvas.manager.full_screen_toggle() # toggle fullscreen mode
#fig.show()
plt.show()

