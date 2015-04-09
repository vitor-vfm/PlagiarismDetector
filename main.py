import sys
from graph import Graph
from time import time
from detector import Detector


if len(sys.argv) > 1:
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
else:
    import curses

    def addstrc(wnd, y, txt):
        wnd.addstr(y, (curses.COLS-len(txt))//2, txt)

    def pick_algo(stdscr):
        stdscr.clear()

        addstrc(stdscr, 2, "Plagiarism Detector")
        addstrc(stdscr, 3, "By Pavlo Malynin and Vitor Mendonca")
        stdscr.addstr(5, 0, "Pick an algorithm:")
        stdscr.addstr(6, 2, "1. Common Sentece Comparison")
        stdscr.addstr(7, 2, "2. Dynamic Programming Subsequence Count")
        stdscr.addstr(8, 2, "3. Suffix Tree Assisted LCS")
        stdscr.addstr(9, 2, "4. TF-IDF")
        stdscr.addstr(11, 2, "5. Quit")
        stdscr.addstr(curses.LINES-1, 0, "Enter command:", curses.A_BLINK)
        stdscr.refresh()
        while True:
            key = stdscr.getkey()
            if key == "5":
                return -1
            else:
                try:
                    algo = int(key)
                    if algo < 5:
                        return algo
                except:
                    continue


    def main(stdscr):
        stdscr.clear()

        addstrc(stdscr, 2, "Plagiarism Detector")
        addstrc(stdscr, 3, "By Pavlo Malynin and Vitor Mendonca")
        stdscr.addstr(5, 0, "Options:")
        stdscr.addstr(6, 2, "1. Full Scan Mode")
        stdscr.addstr(7, 2, "2. Single File Mode")
        stdscr.addstr(9, 2, "3. Quit")
        
        stdscr.addstr(curses.LINES-1, 0, "Enter command:", curses.A_BLINK)
        stdscr.refresh()
        while True:
            key = stdscr.getkey()
            if key == "3":
                break
            elif key == "1":
                algo = pick_algo(stdscr)
                if algo == -1:
                    return
                stdscr.clear()
                addstrc(stdscr, 2, "Plagiarism Detector")
                addstrc(stdscr, 3, "By Pavlo Malynin and Vitor Mendonca")
                stdscr.addstr(5, 0, "Details:")
                stdscr.addstr(6, 2, "Folder: ")
                stdscr.refresh()
                curses.echo()
                folder = stdscr.getstr().decode('utf-8')
                stdscr.addstr(7, 2, "Threshold: ")
                threshold = stdscr.getstr()

                stdscr.clear()
                addstrc(stdscr, 2, "Running....")
                stdscr.refresh()

                startTime = time()
                detector = Detector(folder, float(threshold), algo)
                plagiarisms = detector.run_detection()
                stdscr.clear()
                addstrc(stdscr, 2, "Done in {0} seconds".format(int(time()-startTime)))
                if plagiarisms:

                    stdscr.addstr(5, 0, "Possible plagiarisms:")
                    for i, p in enumerate(plagiarisms[:6]):
                        stdscr.addstr(6+i, 0, "{0}. {1} and {2}".format(i, p[0], p[1]))
                else:
                    stdscr.addstr(5, 0, "It seems like there are no plagiarisms")
                stdscr.getkey()
                return
            elif key == "2":
                algo = pick_algo(stdscr)
                if algo == -1:
                    return
                stdscr.clear()
                addstrc(stdscr, 2, "Plagiarism Detector")
                addstrc(stdscr, 3, "By Pavlo Malynin and Vitor Mendonca")
                stdscr.addstr(5, 0, "Details:")
                curses.echo()
                stdscr.addstr(6, 2, "File: ")
                mainFile = stdscr.getstr().decode('utf-8')
                stdscr.addstr(7, 2, "Folder: ")
                folder = stdscr.getstr().decode('utf-8')
                stdscr.addstr(8, 2, "Threshold: ")
                threshold = stdscr.getstr()

                stdscr.clear()
                addstrc(stdscr, 2, "Running....")
                stdscr.refresh()

                startTime = time()
                detector = Detector(folder, float(threshold), algo, mainFile)
                plagiarisms = detector.run_detection()
                stdscr.clear()
                addstrc(stdscr, 2, "Done in {0} seconds".format(int(time()-startTime)))
                if plagiarisms:

                    stdscr.addstr(5, 0, "Possible plagiarisms:")
                    for i, p in enumerate(plagiarisms[:6]):
                        stdscr.addstr(6+i, 0, "{0}. {1} and {2}".format(i, p[0], p[1]))
                else:
                    stdscr.addstr(5, 0, "It seems like there are no plagiarisms")
                stdscr.getkey()
                return


    stdscr = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()

    main(stdscr)

    curses.nocbreak()
    curses.echo()
    curses.endwin()

