from subprocess import list2cmdline


class Service:
  def __init__(self, *,
               always_restart: bool = False,
               cmd: str,
               description: str = None,
               name: str = None,
               on_boot: bool = False,
               restart_sec: int = None,
               user: str = None,
               ):
    self.always_restart = always_restart
    self.cmd = cmd if type(cmd) == str else list2cmdline(cmd)
    self.description = description
    self.name = name
    self.on_boot = on_boot
    self.restart_sec = restart_sec
    self.user = user
