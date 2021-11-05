"""
Helper script for running flask server and perform DB migrations
"""
import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server, Shell

from conference_management_app import create_app, db, models

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, models=models)


port = os.getenv('PORT', '8081')
manager.add_command("runserver", Server(host="0.0.0.0", port=int(port)))
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def pre_reqs():
    pass


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask_migrate import upgrade

    # migrate database to latest revision
    upgrade()


if __name__ == '__main__':
    manager.run()
