import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app import App


def main():
    application = App()
    sys.exit(application.run())


if __name__ == "__main__":
    main()
