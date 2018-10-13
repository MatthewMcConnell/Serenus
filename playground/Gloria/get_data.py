import sys
from aubio import source, tempo
from numpy import array, ma

def get_pitch(filein):
    from aubio import pitch

    filename = filein

    downsample = 1
    samplerate = 44100 // downsample

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

    total_frames = 0

    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]
        confidence = pitch_o.get_confidence()
        #print("%f %f" % (pitch, confidence))
        pitches += [pitch]
        confidences += [confidence]
        total_frames += read
        if read < hop_s: break

    pitches = array(pitches[1:])
    confidences = array(confidences[1:])
    # times = [t * hop_s for t in range(len(pitches))]
    cleaned_pitches = ma.masked_where(confidences < tolerance, pitches)
    cleaned_pitches = cleaned_pitches[cleaned_pitches.mask == False] # reliable values

    return cleaned_pitches

def get_tempo(filein):
    win_s = 512                 # fft size
    hop_s = win_s // 2          # hop size

    filename = filein

    samplerate = 0

    s = source(filename, samplerate, hop_s)
    samplerate = s.samplerate
    o = tempo("default", win_s, hop_s, samplerate)

    # tempo detection delay, in samples
    # default to 4 blocks delay to catch up with
    delay = 4. * hop_s

    beats = []
    bpm = []

    # total number of frames read
    total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = int(total_frames - delay + is_beat[0] * hop_s)
            #print("beats per minute: %f" % (o.get_bpm()))
            beats.append(this_beat)
            bpm.append(o.get_bpm())
        total_frames += read
        if read < hop_s: break

    return array(bpm)