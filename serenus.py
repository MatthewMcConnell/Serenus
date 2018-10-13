# The main file to run everything from collating all the functions and linking them together

import sys
import importlib
import playground.Gloria.get_data as pitchAndBPM

def main (argv):
    fileName = argv[0]

    # Glorias aubio
    pitch = pitchAndBPM.get_pitch(fileName)
    bpm = pitchAndBPM.get_tempo(fileName)
    
    print(pitch)
    print(bpm)
    # Then put the aubio into serhats transformation algorithm so that it can be used for Sara's vispy visual generation algorithm

    # Finally collate both the transformed aubio data and the speech recognition word data into Sara's vispy algorithm
        # This should check first for command keywords and then convert the aubio data into graphics that are shown
    
      

    return 0;



if __name__ == "__main__":
    main(sys.argv[1:])

