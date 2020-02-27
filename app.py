from flask import Flask

app = Flask(__name__)

from views import *

if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        app.run()
    elif len(sys.argv) > 1:
        if sys.argv[1] == '--debug':
            app.debug = True
            app.run()
        else:
            print('Unknows option')
