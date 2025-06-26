from subprocess import DEVNULL, CalledProcessError, check_call
from typing import Any, List, Sequence

import dotbot


class Pacstall(dotbot.Plugin):
    def can_handle(self, directive: str) -> bool:
        return directive == "pacstall"

    def handle(self, directive: str, packages: List[str]) -> bool:
        success = self._run(["pacstall", "-Up"], "Updating APT") and self._run(
            ["pacstall", "-I"] + packages,
            "Installing the Pacstall packages: {}".format(", ".join(packages)),
        )

        if success:
            self._log.info("Pacstall packages installed successfully")

        return success

    def _run(self, command: Sequence[Any], low_info: str) -> bool:
        self._log.lowinfo(low_info)
        try:
            check_call(command, stdout=DEVNULL, stderr=DEVNULL)
            return True
        except CalledProcessError as e:
            self._log.error(e)
            return False
