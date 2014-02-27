#!env python
from flask.ext.migrate import MigrateCommand
from flask.ext.script import Manager
from microblog.app import create_app

app = create_app("microblog")

manager = Manager(app)
manager.add_command("db", MigrateCommand)


@manager.command
def run_prod():
    app.run(debug=False)


if __name__ == "__main__":
    manager.run()
