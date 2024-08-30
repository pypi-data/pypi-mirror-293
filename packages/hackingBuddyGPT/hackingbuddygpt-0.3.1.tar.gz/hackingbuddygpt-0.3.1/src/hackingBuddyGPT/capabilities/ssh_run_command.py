import re

from dataclasses import dataclass
from invoke import Responder
from io import StringIO
from typing import Tuple

from hackingBuddyGPT.utils import SSHConnection
from hackingBuddyGPT.utils.shell_root_detection import got_root
from .capability import Capability

@dataclass
class SSHRunCommand(Capability):
    conn: SSHConnection
    timeout: int = 10

    def describe(self) -> str:
        return f"give a command to be executed and I will respond with the terminal output when running this command over SSH on the linux machine. The given command must not require user interaction."

    def get_name(self):
        return "exec_command"

    def __call__(self, command: str) -> Tuple[str, bool]:
        if command.startswith(self.get_name()):
            cmd_parts = command.split(" ", 1)
            command = cmd_parts[1]

        sudo_pass = Responder(
            pattern=r'\[sudo\] password for ' + self.conn.username + ':',
            response=self.conn.password + '\n',
        )

        out = StringIO()

        try:
            resp = self.conn.run(command, pty=True, warn=True, out_stream=out, watchers=[sudo_pass], timeout=self.timeout)
        except Exception as e:
            print("TIMEOUT! Could we have become root?")
        out.seek(0)
        tmp = ""
        last_line = ""
        for line in out.readlines():
            if not line.startswith('[sudo] password for ' + self.conn.username + ':'):
                line.replace("\r", "")
                last_line = line
                tmp = tmp + line

        # remove ansi shell codes
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        last_line = ansi_escape.sub('', last_line)

        return tmp, got_root(self.conn.hostname, last_line)
