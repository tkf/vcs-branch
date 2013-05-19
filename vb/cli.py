from .core import BaseApplication, TaskRunnerApp


class InitializeApp(TaskRunnerApp):

    command = 'init'


class CheckoutApp(TaskRunnerApp):

    command = 'checkout'

    def add_arguments(self, parser):
        parser.add_argument('branch')


class VBApp(BaseApplication):

    subappclasses = [InitializeApp, CheckoutApp]

    def __init__(self):
        self.subapps = [c() for c in self.subappclasses]
        self._command_app_map = dict((c.command, c) for c in self.subapps)

    def add_arguments(self, parser):
        subparsers = parser.add_subparsers()
        for subapp in self.subapps:
            subp = subparsers.add_parser(subapp.command)
            subp.set_defaults(command=subapp.command)
            subapp.add_arguments(subp)

    def do_run(self, command, **kwds):
        self.current_app = self._command_app_map[command]
        self.current_app.do_run(**kwds)
