from pyTwistyScrambler import scrambler333, scrambler555, scrambler444, scrambler222, scrambler666, scrambler777
import time

time1 = time.time()
print("\n2x2 Scramble:")
print (scrambler222.get_WCA_scramble())
time2 = time.time()
total = time2 - time1
print("2x2 scramble gen time: " + str(round(total,2)) +"s")

time1 = time.time()
print("\n3x3 Scramble:")
print (scrambler333.get_WCA_scramble())
time2 = time.time()
total = time2 - time1
print("3x3 scramble gen time: " + str(round(total,2)) +"s")

time1 = time.time()
print("\n4x4 Scramble:")
print (scrambler444.get_WCA_scramble())
time2 = time.time()
total = time2 - time1
print("4x4 scramble gen time: " + str(round(total,2)) +"s")

time1 = time.time()
print("\n5x5 Scramble:")
print (scrambler555.get_WCA_scramble())
time2 = time.time()
total = time2 - time1
print("5x5 scramble gen time: " + str(round(total,2)) +"s")

time1 = time.time()
print("\n6x6 Scramble:")
print (scrambler666.get_WCA_scramble())
time2 = time.time()
total = time2 - time1
print("6x6 scramble gen time: " + str(round(total,2)) +"s")

time1 = time.time()
print("\n7x7 Scramble:")
print (scrambler777.get_WCA_scramble())
time2 = time.time()
total = time2 - time1
print("7x7 scramble gen time: " + str(round(total,2)) +"s")
