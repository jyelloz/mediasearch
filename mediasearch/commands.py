# -*- coding: utf-8 -*-

from flask.ext.script import Command, Option


class GeventServer(Command):

    description = 'Run the application with a Gevent server'

    def __init__(self,
                 host='127.0.0.1',
                 port=8000,
                 use_debugger=True,
                 use_reloader=True,
                 passthrough_errors=False):
        self.port = port
        self.host = host
        self.use_reloader = use_reloader
        self.use_debugger = use_debugger
        self.passthrough_errors = passthrough_errors

    def get_options(self):
        return (
            Option(
                '-H',
                '--host',
                dest='host',
                default=self.host
            ),
            Option(
                '-p',
                '--port',
                dest='port',
                type=int,
                default=self.port
            ),
            Option(
                '-d',
                '--no-debug',
                action='store_false',
                dest='use_debugger',
                default=self.use_debugger
            ),
            Option(
                '-r',
                '--no-reload',
                action='store_false',
                dest='use_reloader',
                default=self.use_reloader
            ),
        )

    def handle(self, app, host, port, **kwargs):

        from functools import partial
        from gevent.wsgi import WSGIServer
        from werkzeug.serving import run_with_reloader
        from werkzeug.debug import DebuggedApplication

        use_debugger = kwargs['use_debugger']
        use_reloader = kwargs['use_reloader']

        application = (
            DebuggedApplication(app, True) if use_debugger
            else app
        )

        server = WSGIServer(
            (host, port),
            application,
        ).serve_forever

        f = (
            partial(run_with_reloader, server) if use_reloader
            else server
        )

        f()


class SocketIOServer(GeventServer):

    def handle(self, app, host, port, **kwargs):

        from functools import partial
        from socketio.server import SocketIOServer as WSGIServer
        from werkzeug.serving import run_with_reloader
        from werkzeug.debug import DebuggedApplication
        # from werkzeug.wsgi import SharedDataMiddleware

        use_debugger = False and kwargs['use_debugger']
        use_reloader = kwargs['use_reloader']

        application = (
            DebuggedApplication(app, evalex=True) if use_debugger
            else app
        )

        global server
        server = WSGIServer(
            (host, port),
            application,
            resource='socket.io',
            policy_server=False,
            # policy_listener=(host, port + 10000),
        )

        f = (
            partial(run_with_reloader, server.serve_forever) if use_reloader
            else server.serve_forever
        )

        f()
