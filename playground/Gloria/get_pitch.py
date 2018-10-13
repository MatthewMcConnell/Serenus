import sys
from aubio import source, pitch
from numpy import array, ma

if len(sys.argv) < 2:
    print("Usage: %s <filename> [samplerate]" % sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]

downsample = 1
samplerate = 44100 // downsample
if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

win_s = 4096 // downsample # fft size
hop_s = 512  // downsample # hop size

s = source(filename, samplerate, hop_s)
samplerate = s.samplerate

tolerance = 0.8

pitch_o = pitch("yin", win_s, hop_s, samplerate)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)

pitches = []
confidences = []

# total number of frames read
total_frames = 0

while True:
    samples, read = s()
    pitch = pitch_o(samples)[0]
    confidence = pitch_o.get_confidence()
    print("%f %f" % (pitch, confidence))
    pitches += [pitch]
    confidences += [confidence]
    total_frames += read
    if read < hop_s: break

pitches = array(pitches[1:])
confidences = array(confidences[1:])
times = [t * hop_s for t in range(len(pitches))]
cleaned_pitches = ma.masked_where(confidences < tolerance, pitches)
cleaned_pitches = cleaned_pitches[cleaned_pitches.mask == False] # reliable values