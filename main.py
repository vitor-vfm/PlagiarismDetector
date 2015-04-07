import sys
from graph import Graph
from detector import Detector


# read arguments
directory = sys.argv[1]
threshold = float(sys.argv[2])
algorithm = int(sys.argv[3])

# create detector
detector = Detector(directory, threshold, algorithm)

# run detection
plagiarisms = detector.run_detection()

if plagiarisms:
    print("Possible plagiarisms")
    for i, p in enumerate(plagiarisms[:6]):
        print(i, ": ", p[0], " and ", p[1])
else:
    print("It seems like there are no plagiarisms")
