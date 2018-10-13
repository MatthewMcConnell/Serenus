# Tempo Mapping Algorithm
import numpy as np
from numpy import array
import matplotlib.pyplot as plot

# import sys
# from aubio import source, pitch
# from numpy import array, ma
#
# if len(sys.argv) < 2:
#     print("Usage: %s <filename> [samplerate]" % sys.argv[0])
#     sys.exit(1)
#
# filename = sys.argv[1]
#
# downsample = 1
# samplerate = 44100 // downsample
# if len( sys.argv ) > 2: samplerate = int(sys.argv[2])
#
# win_s = 4096 // downsample # fft size
# hop_s = 512  // downsample # hop size
#
# s = source(filename, samplerate, hop_s)
# samplerate = s.samplerate
#
# tolerance = 0.8
#
# pitch_o = pitch("yin", win_s, hop_s, samplerate)
# pitch_o.set_unit("midi")
# pitch_o.set_tolerance(tolerance)
#
# pitches = []
# confidences = []
#
# # total number of frames read
# total_frames = 0
#
# while True:
#     samples, read = s()
#     pitch = pitch_o(samples)[0]
#     confidence = pitch_o.get_confidence()
#     print("%f %f" % (pitch, confidence))
#     pitches += [pitch]
#     confidences += [confidence]
#     total_frames += read
#     if read < hop_s: break
#
# pitches = array(pitches[1:])
# confidences = array(confidences[1:])
# times = [t * hop_s for t in range(len(pitches))]
# cleaned_pitches = ma.masked_where(confidences < tolerance, pitches)
# cleaned_pitches = cleaned_pitches[cleaned_pitches.mask == False] # reliable values

# Get x values of the sine wave

#time = np.arange(0, 10, 0.1);

# Amplitude of the sine wave is sine of a variable like time

#amplitude = np.sin(time)

# Plot a sine wave using time and amplitude obtained for the sine wave

#plot.plot(amplitude, time)

# Give a title for the sine wave plot

#plot.title('Sine wave')

# Give x axis label for the sine wave plot

#plot.xlabel('Time')

# Give y axis label for the sine wave plot

#plot.ylabel('Amplitude = sin(time)')

#plot.grid(False, which='both')

#plot.axhline(y=0, color='k')

#plot.show()

# Display the sine wave

##plot.show()
def pitchMapping(list):
    # Generate a standard list (of 100 values) for our x-axis
    xValues = array(np.arange(0, len(list)));
    yValues = [];
    # For each value of the input we have, plot a y-val from the list of generic x-vals we have to make a standard Sine
    # Curve, then multiply this y-val by by the input list to transform the amplitude
    for val in range(0,len(list)):
        yValues.append((list[val] * np.sin(xValues[val])))

    #Make the y-val list into a numpy array
    numpyY = array(yValues)

    #Test
    print(numpyY)
    print(xValues)

    plot.plot(yValues, xValues)
    plot.show()

    return numpyY,xValues


a = [x for x in range(-100, 100)]
pitchMapping(a);



