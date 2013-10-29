# -*- coding: utf-8 -*-


def main():

    from gevent import monkey
    monkey.patch_all()

    import logging

    from functools import partial
    from flask.ext.script import Manager

    from .web import create
    from .commands import GeventServer

    logging.basicConfig(level=logging.DEBUG)
    logging.captureWarnings(True)

    class Config(object):

        DEBUG = True
        SITE_TITLE = 'Mediasearch'
        SECRET_KEY = 'secret'
        DATABASE = 'database'

    configured_create = partial(
        create,
        config=Config(),
    )

    manager = Manager(configured_create)
    manager.add_command('rungeventserver', GeventServer())
    manager.run()


if __name__ == '__main__':
    main()
