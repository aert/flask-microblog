#!/usr/bin/env python
from flask import current_app
from flask.ext.migrate import MigrateCommand
from flask.ext.script import Manager
from microblog.factory import create_app


manager = Manager(create_app)
manager.add_command("db", MigrateCommand)


@manager.command
def run_prod():
    current_app.debug = False
    current_app.run("0.0.0.0")


@manager.command
def run_debug():
    current_app.debug = True
    current_app.run("0.0.0.0")


if __name__ == "__main__":
    manager.run()
