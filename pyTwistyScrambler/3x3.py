from pyTwistyScrambler import scrambler335
import os

with open("/home/pi/CubeTimer/scrambles.txt", "a") as scrambleFile:
    print("Generating new 3x3 scramble")
    scrambleFile.write(scrambler333.get_WCA_scramble()+ os.linesep)
    print("Generation complete")
