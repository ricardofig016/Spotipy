# This file serves as the entry point for your application,
# where you initialize the user interface and various modules.
# It's where your application's main event loop is defined.


import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import Window


def main():
    app = QApplication(sys.argv)

    # Initialize your user interface
    window = Window()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
