import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import get_data as aub
from scale import scale
from wavlength import wavlength
import pyaudio, wave
import atexit
import random
import time
import math
import mutagen.wavpack
# Random seed
np.random.seed(29680801)

# Constant declarations

INTERVAL = 10
DROP_COUNT = 50
FILELENGTH = (wavlength("../../80s.wav"))

# Variable to control the pitch up and down
pitch_list = aub.get_pitch("../../80s.wav")
tempo_list = aub.get_tempo("../../80s.wav")


pitch_scaled = scale(pitch_list)
tempo_scaled = scale(tempo_list)
print(len(tempo_list), len(pitch_list))
time_position = 1

pitch_time_ratio = len(pitch_list) / FILELENGTH

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
                  s=rain_drops['size'], lw=0.5, edgecolors='none',
                  facecolors=rain_drops['color'])
T0 = time.time()
print(pitch_time_ratio)

def update(frame_number):

    time_position = math.floor((time.time() - T0) * pitch_time_ratio)
    if time_position >= len(pitch_list):
        return
    # Get an index which we can use to re-spawn the oldest raindrop.
    current_index = frame_number % DROP_COUNT
    print(current_index)

    # Make all colors more transparent as time progresses.
    rain_drops['color'][:, 3] -= 1.0/len(rain_drops)
    rain_drops['color'][:, 3] = np.clip(rain_drops['color'][:, 3], 0, 1)

    # Make all circles bigger.
    rain_drops['size'] += rain_drops['growth']

    r = pitch_scaled[time_position-1]
    g = pitch_scaled[time_position-1]
    b = pitch_scaled[time_position-1]#pitch_list[int(time_position)]/50.0
    #g = pitch_list[int(time_position)]/100.0
    #b = pitch_list[int(time_position)]/100.0
    # Pick a new position for oldest rain drop, resetting its size,
    # color and growth factor.
    #print(r,g, b)
    rain_drops['position'][current_index, 0] = np.random.uniform(0, 1, 1)
    rain_drops['position'][current_index, 1] = np.random.uniform(0.4+pitch_list[time_position-1]-pitch_list[time_position], 0.6+pitch_list[time_position-1]-pitch_list[time_position], 1)
    rain_drops['size'][current_index] = 5
    rain_drops['color'][current_index] = (r, 0, 0, 1)
    rain_drops['growth'][current_index] = np.random.uniform(50, 200)

    # Update the scatter collection, with the new colors, sizes and positions.
    scat.set_facecolors(rain_drops['color'])
    scat.set_sizes(rain_drops['size'])
    scat.set_offsets(rain_drops['position'])

# Construct the animation, using the update function as the animation director.
animation = FuncAnimation(fig, update, interval=INTERVAL)
fig.patch.set_facecolor((0.8, 0.9, 0.8))
fig.canvas.manager.full_screen_toggle() # toggle fullscreen mode
fig.show()
plt.show()