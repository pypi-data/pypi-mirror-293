from cleo.application import Application

from systemdcli.init_command import InitCommand

application = Application()
application.add(InitCommand())

def main():
    application.run()
