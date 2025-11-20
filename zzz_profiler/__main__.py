import sys
import os

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    sys.path.insert(0, os.path.abspath(os.path.join(application_path, '..')))
else:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from zzz_profiler.qt_app import main

if __name__ == '__main__':
    main()