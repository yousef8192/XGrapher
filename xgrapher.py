"""
XGrapher

@ Author: Yousef Mohammed
@ All rights reserved (or....???)

"""

from _XGRAPHER_GUI_ import *
from _XGRAPHER_LOGIC_ import *
import sys  # for system related operations


# This condition is essential to avoid executing this code in test files
if __name__ == '__main__':
    # create a new application which represents the XGrapher Application (sys.argv represents a set of command line arguments)
    main_application = QApplication(sys.argv)

    # Compute screen dimensions to set XGrapher's minimum window size accordingly
    SCREEN_HEIGHT = main_application.primaryScreen().size().height()
    SCREEN_WIDTH  = main_application.primaryScreen().size().width()

    # create the main window for the XGrapher Application and display it
    main_window = XGrapherWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    main_window.show()

    # start the event loop for the XGrapher application
    main_application.exec_()


