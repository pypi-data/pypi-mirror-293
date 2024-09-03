import os
import subprocess
import time
from pathlib import Path

from cleo.commands.command import Command
from cleo.io.inputs.option import Option


class InitCommand(Command):
    name = 'init'
    description = 'Init systemd unit'

    options: list[Option] = []

    # arguments: list[Argument] = [
    #     argument(, 'systemd-path', 'The path to the systemd directory', optional=True)
    # ]

    def handle(self):
        cwd = os.getcwd()
        currentFolderName = cwd.split("/")[-1]
        currentUser = os.getlogin()

        working_directory = self.ask("Enter the working directory (default: cwd): ", cwd)
        exec_start = self.ask("Enter the command to run: ")
        if not exec_start:
            self.line("\n<error>Aborted</error>\n")
            exit(1)

        self.line(
            '\n<info>Now I will run the command to check if it works, finish the process when you\'re done</info>\n')
        time.sleep(1)

        try:
            _cwd = os.getcwd()
            os.chdir(working_directory)
            subprocess.run(exec_start, check=True, shell=True)
            os.chdir(_cwd)
            # subprocess.Popen(exec_start, cwd=working_directory, shell=True)
        except subprocess.SubprocessError:
            self.line("\n<error>Error: The command failed to run. Please check the command and try again.</error>")
            exit(1)

        if not self.confirm("\nDid the command run correctly?", True):
            self.line("\n<error>Aborted</error>\n")
            exit(1)

        name = self.ask("Enter the service unit name: ", currentFolderName)
        description = self.ask(f"Enter the service description (default: {name}): ", default=name)
        user = self.ask(f"Enter the user to run the service as (default: {currentUser}): ", currentUser)
        group = self.ask("Enter the group to run the service as (default: nogroup): ", 'nogroup')

        self.line("\n<info> -- Creating systemd unit file</info>")

        service_file_path = create_systemd_unit_file(name, description, exec_start, user, group, working_directory)

        if self.confirm("\nDo you want to enable and start the service?", True):
            self.line("\n<info> -- Enabling and starting the service</info>")
            enable_and_start_service(service_file_path)

        self.line('\n<info>Done</info>\n')


SYSTEMD_PATH = "/etc/systemd/system"


def create_systemd_unit_file(service_name, description, exec_start, user, group, working_directory):
    """Create the systemd unit file."""
    service_file_path = Path(SYSTEMD_PATH) / (service_name + '.service')

    content = f"""
[Unit]
Description={description}

[Service]
ExecStart={exec_start}
Restart=always
User={user}
Group={group}
Environment=PATH=/usr/bin:/usr/local/bin
WorkingDirectory={working_directory}

[Install]
WantedBy=multi-user.target
    """.strip()

    # Write the service file
    with open(service_file_path, 'w') as service_file:
        service_file.write(content)

    print(f"Systemd service file created at {service_file_path}")
    return service_file_path


def enable_and_start_service(service_file_path):
    """Enable and start the systemd service."""
    service_name = service_file_path.name
    subprocess.run(["systemctl", "daemon-reload"], check=True)
    subprocess.run(["systemctl", "enable", service_name], check=True)
    subprocess.run(["systemctl", "start", service_name], check=True)
    print(f"Service {service_name} has been enabled and started.")
