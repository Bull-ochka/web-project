from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from views import *

if __name__ == '__main__':
    import sys

    if len(sys.argv) == 1:
        app.run()

    elif len(sys.argv) == 2:
        if sys.argv[1] == '--debug':
            app.debug = True
            app.run()
        else:
            print('Unknows option')

    else:
        print('Too many options')
