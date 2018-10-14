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


get_pitches = []
bpm = []
volume = []

def graph(mode, filename):

    CHUNK = 1024
    total_frames = 0
    RATE = 44100 
    FORMAT = pyaudio.paFloat32 # We use 16bit format per sample
    CHANNELS = 1        
    RECORD_SECONDS = 0.1

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
    np.random.seed(19680801)

    init_pitches = get_pitch(stream, RATE, CHUNK)
    if init_pitches == -1:
        pass #sort out

    # Variable to control the pitch up and down
    
    yPitch = init_pitches
    yPitchIndex = 1

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
    rain_drops['growth'] = np.random.uniform(50, 200, n_drops)

    # Construct the scatter which we will update during animation
    # as the raindrops develop.
    scat = ax.scatter(rain_drops['position'][:, 0], rain_drops['position'][:, 1],
                    s=rain_drops['size'], lw=0.5, edgecolors=rain_drops['color'],
                    facecolors='none')


    def update(frame_number):
        nonlocal yPitchIndex
        nonlocal yPitch
        nonlocal rain_drops
        nonlocal stream

        up_pitches = get_pitch(stream, RATE, CHUNK)
        if up_pitches == -1:
            pass #sort out
        #print(up_pitches)

        # Get an index which we can use to re-spawn the oldest raindrop.
        current_index = frame_number % n_drops

        # Make all colors more transparent as time progresses.
        rain_drops['color'][:, 3] -= 1.0/len(rain_drops)
        rain_drops['color'][:, 3] = np.clip(rain_drops['color'][:, 3], 0, 1)

        # Make all circles bigger.
        rain_drops['size'] += rain_drops['growth']

        
        # if (yPitchIndex >= len(yPitch)-1):
        #     yPitchIndex = 1
        # else:
        #     yPitchIndex += 1

        # Pick a new position for oldest rain drop, resetting its size,
        # color and growth factor.
        rain_drops['position'][current_index, 0] = np.random.uniform(0, 1, 1)
        #rain_drops['position'][current_index, 1] = np.random.uniform(0.4+yPitch[yPitchIndex-1]-yPitch[yPitchIndex], 0.6+yPitch[yPitchIndex-1]-yPitch[yPitchIndex], 1)
        rain_drops['size'][current_index] = 5
        rain_drops['color'][current_index] = (0, 0, 0, 1)
        rain_drops['growth'][current_index] = np.random.uniform(50, 200)

        # Update the scatter collection, with the new colors, sizes and positions.
        scat.set_edgecolors(rain_drops['color'])
        scat.set_sizes(rain_drops['size'])
        scat.set_offsets(rain_drops['position'])


    # Construct the animation, using the update function as the animation director.
    animation = FuncAnimation(fig, update, repeat = False, interval = 10)

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
    tolerance = 0.8
    win_s = 4096 # fft size
    hop_s = CHUNK # hop size
    pitch_o = aubio.pitch("yinfast", win_s, hop_s, RATE)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)

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
        