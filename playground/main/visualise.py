import pyaudio
import sys
import numpy as np
import aubio
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import Gloria.get_data as aub
import wave
import atexit
import time
from Gloria.scale import listscale, rgbscale
import pyaudio, wave
import atexit, random, time, math

CHUNK = 1024
total_frames = 0
RATE = 44100 
FORMAT = pyaudio.paFloat32 # We use 16bit format per sample
CHANNELS = 1        
RECORD_SECONDS = 0.1

get_pitches = []
bpm = []
volume = []

tolerance = 0.8
win_s = 4096 # fft size
hop_s = CHUNK # hop size
pitch_o = aubio.pitch("yinfast", win_s, hop_s, RATE)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)

INTERVAL = 10
DROP_COUNT = 50

## CONSTANTS
VOLUME_SCALING = 0.8

def graph(mode, filename):

    if mode == "live":
        # set up live stream

        audio = pyaudio.PyAudio()

        # start Recording
        stream = audio.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK)#,
                            #frames_per_buffer=CHUNK)

        # Open the connection and start streaming the data
        stream.start_stream()

    else:
        # set up file from audio stream

        audio_file = wave.open(filename, 'rb')

        p = pyaudio.PyAudio()

        # open stream (2)
        stream = p.open(format=p.get_format_from_width(audio_file.getsampwidth()),
                        channels=audio_file.getnchannels(),
                        rate=audio_file.getframerate(),
                        input=True)


        # stream = p.open(format=FORMAT,
        #                 channels=CHANNELS,
        #                 rate=RATE,
        #                 output=True,
        #                 frames_per_buffer=CHUNK) # frames_per_buffer=CHUNK_SIZE


    ################### 
    #in_data = stream.read(CHUNK)

    # get stats
    # > pitch
    # > tempo?
    # > volume?


    # Fixing random state for reproducibility
    #np.random.seed(19680801)

    

    # Variable to control the pitch up and down
    if mode == "file":
        yPitch = aub.get_pitch(filename) # yPitch       
        TEMPO_LIST = aub.get_tempo(filename)
        VOLUME = listscale(aub.get_volume(filename))

        PITCH_SCALED = listscale(yPitch)
        TEMPO_SCALED = listscale(TEMPO_LIST)
        print(len(TEMPO_LIST), len(yPitch))
        # PITCH_TIME_RATIO = len(yPitch) / FILELENGTH
        # VOLUME_TIME_RATIO = len(VOLUME) / FILELENGTH

    else:
        yPitch = get_pitch(stream, RATE, CHUNK)
        if yPitch == -1:
            pass #sort out

    yPitchIndex = 1

    # Creates a figurue and removes the toolbar.
    plt.rcParams['toolbar'] = 'None'
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
    rain_drops['position'] = np.random.uniform(0.25, 0.50, (DROP_COUNT, 2))
    rain_drops['growth'] = np.random.uniform(50, 200, DROP_COUNT)

    # Construct the scatter which we will update during animation
    # as the raindrops develop.
    scat = ax.scatter(rain_drops['position'][:, 0], rain_drops['position'][:, 1],
                    s=20, lw=0.5, edgecolors='none',
                    facecolors=rain_drops['color'])
    T0 = time.time()


    def update(frame_number):
        nonlocal yPitchIndex
        nonlocal yPitch
        nonlocal rain_drops
        nonlocal stream

        if mode == "live":
            yPitch = get_pitch(stream, RATE, CHUNK)
            if yPitch == -1:
                pass #sort out
        print(yPitch)

        # Get an index which we can use to re-spawn the oldest raindrop.
        current_index = frame_number % n_drops

        # Make all colors more transparent as time progresses.
        rain_drops['color'][:, 3] -= 1.0/len(rain_drops)
        rain_drops['color'][:, 3] = np.clip(rain_drops['color'][:, 3], 0, 1)

        # Make all circles bigger.
        rain_drops['size'] += rain_drops['growth']

        
        if (yPitchIndex >= len(yPitch)-1):
            yPitchIndex = 1
        else:
            yPitchIndex += 1

        r = PITCH_SCALED[yPitchIndex]
        g = PITCH_SCALED[yPitchIndex]
        b = PITCH_SCALED[yPitchIndex]

        # Pick a new position for oldest rain drop, resetting its size,
        # color and growth factor.
        rain_drops['position'][current_index, 0] = np.random.uniform(0, 1, 1)
        rain_drops['position'][current_index, 1] = np.random.uniform(0.4-VOLUME[yPitchIndex] * VOLUME_SCALING, 0.6-VOLUME[yPitchIndex] * VOLUME_SCALING, 1)
        rain_drops['size'][current_index] = 5
        rain_drops['color'][current_index] = (r, 0, 0, 1)
        rain_drops['growth'][current_index] = np.random.uniform(50, 200)

        # Update the scatter collection, with the new colors, sizes and positions.
        scat.set_edgecolors(rain_drops['color'])
        scat.set_sizes(rain_drops['size'])
        scat.set_offsets(rain_drops['position'])


    # Construct the animation, using the update function as the animation director.
    animation = FuncAnimation(fig, update, repeat = False, interval = 10)
    fig.patch.set_facecolor((0.8, 0.9, 0.8))

    plt.show()

    ################### 

    if mode == "live":
        stream.stop_stream()

    # close stream
    stream.close()

    if mode == "live":
        audio.terminate()




def get_pitch(stream, RATE, CHUNK):
        # setup pitch

    ### Ignore tempo for now
    # setup tempo
    #tempo_o = aubio.tempo("default", 2048, 2048 // 2, RATE)

    try:
        audiobuffer = stream.read(CHUNK)
    except:
        return -1

    signal = np.nan_to_num(np.fromstring(audiobuffer, dtype=np.float32))

    pitch = pitch_o(signal)[0] 
    confidence = pitch_o.get_confidence()

    

    if (confidence > -1):
        get_pitches.append(pitch)

        if (len(get_pitches) > 1):
            pass
        # print("{} / {}".format(pitch,confidence))

    print(signal)

    # is_beat = tempo_o(signal)
    # if is_beat:
    #     bpm.append(tempo_o.get_bpm())

    #volume.append(np.sum(signal**2)/len(signal))

    # except KeyboardInterrupt:
    # print("*** Ctrl+C pressed, exiting")
    # break

    return get_pitches
        