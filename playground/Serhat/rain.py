import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Fixing random state for reproducibility
np.random.seed(19680801)


# Variable to control the pitch up and down
yPitch = 0

# Create new Figure and an Axes which fills it.

fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0, 1), ax.set_xticks([])
ax.set_ylim(0, 1), ax.set_yticks([])

# Create rain data
n_drops = 50
rain_drops = np.zeros(n_drops, dtype=[('position', float, 2),
                                      ('size',     float, 1),
                                      ('growth',   float, 1),
                                      ('color',    float, 4)])

# Initialize the raindrops in random positions and with
# random growth rates.
rain_drops['position'] = np.random.uniform(0, 1, (n_drops, 2))
rain_drops['growth'] = np.random.uniform(100, 800, n_drops)

# Construct the scatter which we will update during animation
# as the raindrops develop.
scat = ax.scatter(rain_drops['position'][:, 0], rain_drops['position'][:, 1],
                  s=rain_drops['size'], lw=0.5, edgecolors='none',
                  facecolors=rain_drops['color'])
plt.style.use('dark_background')
def update(frame_number):
    # Get an index which we can use to re-spawn the oldest raindrop.
    current_index = frame_number % n_drops

    # Make all colors more transparent as time progresses.
    rain_drops['color'][:, 3] -= 1.0/len(rain_drops)
    rain_drops['color'][:, 3] = np.clip(rain_drops['color'][:, 3], 0, 1)

    # Make all circles bigger.
    rain_drops['size'] += rain_drops['growth']

    global yPitch
    if (yPitch >= 1):
        yPitch = 0
    else:
        yPitch += 0.01 

    # Pick a new position for oldest rain drop, resetting its size,
    # color and growth factor.
    rain_drops['position'][current_index, 0] = np.random.uniform(0, 1, 1)
    rain_drops['position'][current_index, 1] = np.random.uniform(0+yPitch, 0.01+yPitch, 1)
    rain_drops['size'][current_index] = 5
    #if(tempo[index] < 80):
    #    rain_drops['color'][current_index] = (0, 1, 0, 1)
    #elif(tempo[index] > 160):
    #    rain_drops['color'][current_index] = (1, 0, 0, 1)
    #else:
     #   rain_drops['color'][current_index] =
    rain_drops['color'][current_index] = (0, 0, 1, 1)
    rain_drops['growth'][current_index] = np.random.uniform(50, 200)
    # Update the scatter collection, with the new colors, sizes and positions.
    scat.set_edgecolors(rain_drops['color'])
    scat.set_sizes(rain_drops['size'])
    scat.set_offsets(rain_drops['position'])


# Construct the animation, using the update function as the animation director.
animation = FuncAnimation(fig, update, interval=1)
plt.show()