import sys
from graph import Graph
from detector import Detector


# read arguments
directory = sys.argv[1]
sequence_size = int(sys.argv[2])
num_sequences = int(sys.argv[3])

# create detector
detector = Detector(directory, sequence_size, num_sequences)

# run detection
plagiarisms = detector.run_detection(1)

if plagiarisms:
    print("Possible plagiarisms")
    for i, p in enumerate(plagiarisms):
        print(i, ": ", p[0], " and ", p[1])
else:
    print("It seems like there are no plagiarisms")
