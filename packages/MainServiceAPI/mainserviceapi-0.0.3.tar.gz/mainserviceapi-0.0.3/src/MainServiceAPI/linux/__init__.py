import os
import sys
from ..objects import Service
from configparser import RawConfigParser
from MainShortcuts2 import ms
SERVICES_DIR = "/etc/systemd/system"
WRAPPER_PATH = os.path.dirname(os.path.dirname(__file__)) + "/wrapper.py"


def parse(text: str) -> Service:
  """Прочитать текст сервиса"""
  cfg = RawConfigParser()
  cfg.read_string(text)
  kw = {}
  if "Install" in cfg:
    cat = cfg["Install"]
    if "alias" in cat:
      kw["name"] = cat["alias"]
    if cat.get("wantedby") == "multi-user.target":
      kw["on_boot"] = True
  if "Service" in cfg:
    cat = cfg["Service"]
    if cat.get("restart") == "always":
      kw["always_restart"] = True
    kw["cmd"] = cat["execstart"]
    if "restartsec" in cat:
      kw["restart_sec"] = float(cat["restartsec"])
    if "user" in cat:
      kw["user"] = cat["user"]
  if "Unit" in cfg:
    cat = cfg["Unit"]
    if "description" in cat:
      kw["description"] = cat["description"]
  return Service(**kw)


def unparse(svc: Service) -> str:
  """Собрать текст для файла `.service`"""
  data = {"Install": {}, "Service": {}, "Unit": {}}
  if svc.always_restart:
    data["Service"]["Restart"] = "always"
  data["Service"]["ExecStart"] = svc.cmd
  if svc.description:
    data["Unit"]["Description"] = svc.description.replace("\n", "\\n")
  if svc.name:
    data["Install"]["Alias"] = svc.name
  if svc.on_boot:
    data["Install"]["WantedBy"] = "multi-user.target"
    data["Unit"]["After"] = "network.target"
  if svc.restart_sec:
    data["Service"]["RestartSec"] = str(svc.restart_sec)
  if svc.user:
    data["Service"]["User"] = svc.user
  data["Service"]["Type"] = "simple"
  lines = []
  for cat in data:
    if len(data[cat]) > 0:
      lines.append("[%s]" % cat)
      for item in data[cat]:
        lines.append("%s=%s" % (item, data[cat][item]))
      lines.append("")
  return "\n".join(lines)


def read(path: str) -> Service:
  """Прочитать файл сервиса"""
  return parse(ms.file.read(path))


def write(svc: Service, reload: bool = False, *, filename: str = None, path: str = None):
  """Записать файл сервиса в папку сервисов или по указанному пути"""
  if path is None:
    if filename is None:
      if svc.name is None:
        raise ValueError("The service has no name. Indicate the file name to recording the service")
      filename = svc.name
    if not filename.lower().endswith(".service"):
      filename += ".service"
    path = SERVICES_DIR + "/" + filename
  ms.file.write(path, unparse(svc))
  if reload:
    ms.proc.call("systemctl", "daemon-reload")
  return path


def make_wrapper(name: str, args: list[str], *,
                 clear_env: bool = False,
                 cwd: str = None,
                 data_dir: str = None,
                 env: dict[str, str] = None,
                 exe: str = None,
                 reload: bool = False,
                 stderr: str = None,
                 stdin: str = None,
                 stdout: str = None,
                 **svc_kw) -> str:
  if data_dir is None:
    data_dir = SERVICES_DIR + "/MainServiceAPI"
  ms.dir.create(data_dir)
  data = {"format": 1}
  data["args"] = list(args)
  data["clear_env"] = bool(clear_env)
  if not cwd is None:
    data["cwd"] = ms.path.path2str(cwd, True)
  if not env is None:
    data["env"] = dict(env)
  if not exe is None:
    data["exe"] = ms.path.path2str(exe, True)
  if not stderr is None:
    data["stderr"] = ms.path.path2str(stderr, True)
  if not stdin is None:
    data["stdin"] = ms.path.path2str(stdin, True)
  if not stdout is None:
    data["stdout"] = ms.path.path2str(stdout, True)
  filepath = "%s/%s-wrapper.json" % (data_dir, name)
  ms.json.write(filepath, {"MainServiceAPI/wrapper": data})
  svc_kw["name"] = name
  svc_kw["cmd"] = [sys.executable, WRAPPER_PATH, filepath]
  return os.path.basename(write(Service(**svc_kw), reload=reload))
