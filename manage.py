#!flask/bin/python
from app import app
from flask.ext.script import Manager

# app.run(debug = True, host='0.0.0.0', port=8001)


manager = Manager(app)


@manager.command
def run():
    """Run in local machine."""

    app.run(host='0.0.0.0',port=80,debug=True)




manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()