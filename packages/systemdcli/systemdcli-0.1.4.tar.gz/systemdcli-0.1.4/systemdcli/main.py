from cleo.application import Application

from init_command import InitCommand

application = Application()
application.add(InitCommand())


def main():
    application.run()
