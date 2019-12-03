""" Clustersitter """
__author__ = "titus"

import os

from app import app
from flask_script import Manager, Server, Shell

def generate_shell_context():
    return {
        'app': app,
        'db': db
    }

manager = Manager(app)

manager.add_command("runserver", Server(threaded=True))
manager.add_command('shell', Shell(make_context=generate_shell_context))

if __name__ == '__main__':
    manager.run()
