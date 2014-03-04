#!/usr/bin/env python
from flask.ext.migrate import MigrateCommand
from flask.ext.script import Manager
from microblog.app import create_app


from microblog import models

app = create_app()

manager = Manager(app)
manager.add_command("db", MigrateCommand)


@manager.command
def run_prod():
    app.debug = False
    app.configure()
    app.run("0.0.0.0")


@manager.command
def run_debug():
    app.debug = True
    app.configure()
    app.run("0.0.0.0")


if __name__ == "__main__":
    manager.run()
