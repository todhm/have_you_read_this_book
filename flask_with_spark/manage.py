# Set the path
import os
from flask_script import Manager, Server
from flask import session
from application import create_app


app = create_app()
manager = Manager(app)

#Turn on debugger by default and reloader

manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = os.getenv('IP', '0.0.0.0'),
    port = int(os.getenv('PORT', 5000)))
)

if __name__ == "__main__":
    manager.run()
