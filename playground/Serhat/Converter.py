# Tempo Mapping Algorithm
import numpy as np
from numpy import array
import matplotlib.pyplot as plot

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
def tempoMap(list):
    # Generate a standard list (of 100 values) for our x-axis
    xValues = array(np.arange(0, 10, 0.1));
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

    plot.plot(xValues, yValues)
    plot.show()
    
    return numpyY,xValues

a = [x for x in range(0, 100)]
tempoMap(a);


