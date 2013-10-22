from flask_failsafe import failsafe


@failsafe
def create(config=None):

    from flask import Flask
    from . import ui

    application = Flask(__name__)
    application.config.from_object(config)

    application.register_blueprint(ui.mediasearch)

    return application
